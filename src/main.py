import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

import httpx
from bilibili_api import Danmaku, live, user
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from .config import setting
from .credential import get_credential
from .data import get_date_flag, init_db, set_date_flag


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_db()
    await load()
    asyncio.create_task(RoomObj.connect())
    asyncio.create_task(health())
    yield
    # 关闭时执行（如果需要清理资源）


app = FastAPI(lifespan=lifespan)

# 添加全局锁
gift_lock = asyncio.Lock()


class Gift(BaseModel):
    id: int
    num: int
    price: int = 0
    name: str = ""


CredentialObj = get_credential()
RoomObj = live.LiveDanmaku(setting.room_id, credential=CredentialObj)
GiftObj = Gift(id=setting.target_gift_id, num=setting.target_gift_num)
LiveRoomObj = live.LiveRoom(setting.room_id, CredentialObj)


async def bark(message: str):
    if not setting.bark_key:
        return
    async with httpx.AsyncClient() as client:
        data = {
            "icon": setting.bark_icon,
        }
        await client.get(
            f"https://api.day.app/{setting.bark_key}/{message}", params=data
        )


@RoomObj.on("LIVE")
async def on_live(event):
    logger.info(
        f"直播间开播了，将在{setting.delay}秒后送出{GiftObj.num}个{GiftObj.name}，价值{GiftObj.price * GiftObj.num / 1000}元"
    )

    # 先检查今天是否已经执行过
    if await has_executed_today():
        logger.info("今天已经送过礼物了")
        return

    # 等待延迟时间
    await asyncio.sleep(setting.delay)

    # 再次检查（防止在等待期间其他协程已经执行）
    async with gift_lock:
        if await has_executed_today():
            logger.info("今天已经送过礼物了")
            return

        try:
            await LiveRoomObj.send_danmaku(Danmaku(setting.greeting))
        except Exception as e:
            logger.error(f"发送弹幕失败: {e}")
        try:
            result = await LiveRoomObj.send_gift_gold(
                uid=setting.dedeuserid,
                gift_id=GiftObj.id,
                gift_num=GiftObj.num,
                price=GiftObj.price,
            )
        except Exception as e:
            logger.error(f"送礼物失败: {e}")
            return
        await set_last_execution_date()
        logger.info(f"送礼物成功: {result}")
        await bark("送礼物成功")


async def set_last_execution_date():
    await set_date_flag(datetime.now().strftime("%Y-%m-%d"))


async def has_executed_today() -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    return await get_date_flag(today)


async def load():
    gift_config = await live.get_gift_config(room_id=setting.room_id)
    for idx, gift in enumerate(gift_config["list"]):
        if gift["id"] == GiftObj.id:
            GiftObj.price = gift["price"]
            GiftObj.name = gift["name"]
            logger.info(
                f"找到{GiftObj.id}号礼物{GiftObj.name}，单价为{GiftObj.price // 100}电池 ，折合人民币{GiftObj.price / 1000}元"
            )
            break
    if not GiftObj.price:
        logger.error(f"未找到礼物配置 {GiftObj.id}")
        exit(1)
    account = user.User(CredentialObj.dedeuserid, CredentialObj)
    user_info = await account.get_user_info()
    logger.info(f"用户名称：{user_info['name']}")
    status = await LiveRoomObj.get_room_info()
    logger.info(f"主播名称：{status['anchor_info']['base_info']['uname']}")
    await bark("启动成功")


async def health():
    while True:
        await asyncio.sleep(10)
        status = RoomObj.get_status()
        if status == live.LiveDanmaku.STATUS_CLOSED:
            logger.error("直播间已关闭")
            os._exit(1)
