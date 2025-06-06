import asyncio
import logging
import platform
from datetime import datetime

import httpx
from bilibili_api import live, user, Danmaku
from pydantic import BaseModel

from config import ConfigObj
from credential import get_credential
from data import get_date_flag, init_db, set_date_flag

logger = logging.getLogger(f"LiveDanmaku_{ConfigObj.room_id}")


class Gift(BaseModel):
    id: int
    num: int
    price: int = 0
    name: str = ''


CredentialObj = get_credential()
RoomObj = live.LiveDanmaku(ConfigObj.room_id, credential=CredentialObj)
GiftObj = Gift(id=ConfigObj.target_gift_id, num=ConfigObj.target_gift_num)
LiveRoomObj = live.LiveRoom(ConfigObj.room_id, CredentialObj)


async def bark(message: str):
    if not ConfigObj.bark_key:
        return
    async with httpx.AsyncClient() as client:
        data = {
            "icon": ConfigObj.bark_icon,
        }
        await client.get(f"https://api.day.app/{ConfigObj.bark_key}/{message}", params=data)


@RoomObj.on("LIVE")
async def on_live(event):
    logger.info(
        f"直播间开播了，将在{ConfigObj.delay}秒后送出{GiftObj.num}个{GiftObj.name}，价值{GiftObj.price * GiftObj.num / 1000}元")
    await asyncio.sleep(ConfigObj.delay)
    if has_executed_today():
        logger.info("今天已经送过礼物了")
        return
    try:
        await LiveRoomObj.send_danmaku(Danmaku(ConfigObj.greeting))
    except Exception as e:
        logger.error(f"发送弹幕失败: {e}")
    try:
        result = await LiveRoomObj.send_gift_gold(uid=CredentialObj.dedeuserid, gift_id=GiftObj.id,
                                                  gift_num=GiftObj.num, price=GiftObj.price)
    except Exception as e:
        logger.error(f"送礼物失败: {e}")
        return
    set_last_execution_date()
    logger.info(f"送礼物成功: {result}")
    await bark("送礼物成功")



async def set_last_execution_date():
    await set_date_flag(datetime.now().strftime('%Y-%m-%d'))


async def has_executed_today() -> bool:
    today = datetime.now().strftime('%Y-%m-%d')
    return await get_date_flag(today)


async def load():
    gift_config = await live.get_gift_config(room_id=ConfigObj.room_id)
    for idx, gift in enumerate(gift_config['list']):
        if gift['id'] == GiftObj.id:
            GiftObj.price = gift['price']
            GiftObj.name = gift['name']
            logger.info(
                f"找到{GiftObj.id}号礼物“{GiftObj.name}”，单价为{GiftObj.price // 100}电池 ，折合人民币{GiftObj.price / 1000}元")
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


async def main():
    await init_db()
    await load()
    await RoomObj.connect()

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
