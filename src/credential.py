import json
import os.path
import platform
from typing import List, Optional

from bilibili_api import Credential
from pydantic import BaseModel
from .config import ConfigObj

class Cookie(BaseModel):
    expires: int
    http_only: int
    name: str
    secure: int
    value: str


class CookieInfo(BaseModel):
    cookies: List[Cookie]
    domains: List[str]


class TokenInfo(BaseModel):
    access_token: str
    expires_in: int
    mid: int
    refresh_token: str


class CookiesData(BaseModel):
    cookie_info: CookieInfo
    sso: List[str]
    token_info: TokenInfo
    platform: str


def load_credential() -> Optional[Credential]:
    try:
        with open(ConfigObj.cookies_path, 'r') as f:
            data: CookiesData = CookiesData(**json.load(f))
    except FileNotFoundError:
        return None

    sessdata = ''
    bili_jct = ''
    dedeuserid = ''
    for cookie in data.cookie_info.cookies:
        if cookie.name == 'SESSDATA':
            sessdata = cookie.value
        elif cookie.name == 'bili_jct':
            bili_jct = cookie.value
        elif cookie.name == 'DedeUserID':
            dedeuserid = cookie.value
        else:
            continue
    if not sessdata or not bili_jct or not dedeuserid:
        return None
    return Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3="0EAE94CF-F55C-2A23-37CB-46686BE0626549996infoc",
                      dedeuserid=dedeuserid)




def get_credential(refresh: bool = False) -> Credential:
    if not refresh:
        credential = load_credential()
    else:
        credential = None
    biliup_cmd = "bin/biliup login"
    if platform.system() == 'Windows':
        biliup_cmd = r"bin\biliup.exe login"
    if not credential:
        print('请先登录')
        os.system(biliup_cmd)
        credential = load_credential()
    if not credential:
        print('登录失败')
        exit(1)
    if os.path.exists("qrcode.png"):
        os.remove("qrcode.png")
    return credential
