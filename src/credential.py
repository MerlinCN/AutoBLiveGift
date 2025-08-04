import json
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
    cookies = load_from_cc()
    return Credential(
        bili_jct=cookies["bili_jct"],
        buvid3=cookies["buvid3"],
        dedeuserid=cookies["DedeUserID"],
        sessdata=cookies["SESSDATA"],
    )
