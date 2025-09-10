import json
from pathlib import Path
from typing import Dict

from bilibili_api import Credential
from PyCookieCloud import PyCookieCloud
from PyCookieCloud.PyCryptoJS import decrypt

from .config import setting


def load_from_cc() -> Dict[str, str | int]:
    cc = PyCookieCloud(
        setting.cookie_cloud_url,
        setting.cookie_cloud_uuid,
        setting.cookie_cloud_password,
    )
    encrypted_data = cc.get_encrypted_data()
    decrypted_data = decrypt(encrypted_data, cc.get_the_key().encode("utf-8")).decode(
        "utf-8"
    )
    decrypted_data = json.loads(decrypted_data)
    cookies = decrypted_data["cookie_data"][".bilibili.com"]
    result = {}
    for cookie in cookies:
        result[cookie["name"]] = cookie["value"]
    return result


def get_credential() -> Credential:
    cookies_path = Path("./cookies.json")
    with open(cookies_path, "r") as f:
        cookies = json.load(f)
    cookies = cookies[0]["origin"]["cookie_info"]["cookies"]
    cookie_kv = {}
    for cookie in cookies:
        cookie_kv[cookie["name"]] = cookie["value"]
    return Credential(
        bili_jct=cookie_kv["bili_jct"],
        buvid3="BD89AF90-A985-A949-7C2A-E05C6AB0551C05830infoc",
        dedeuserid=cookie_kv["DedeUserID"],
        sessdata=cookie_kv["SESSDATA"],
    )
