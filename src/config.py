import os
from typing import Optional

from pydantic import BaseModel, Field
from ruamel.yaml import YAML


# 定义配置模型
class Config(BaseModel):
    room_id: int = Field(default=6846214, description="直播间ID")
    target_gift_id: int = Field(default=31036, description="要送的礼物ID（默认是小花花）")
    target_gift_num: int = Field(default=1, description="要送的礼物数量")
    delay: int = Field(default=60, description="送礼物延时（秒）")
    debug: bool = Field(default=False, description="是否开启调试模式")


CONFIG_FILE_PATH = 'config.yaml'
yaml = YAML()


def load_or_create_config() -> Optional[Config]:
    if not os.path.exists(CONFIG_FILE_PATH):
        config = Config()
        with open(CONFIG_FILE_PATH, 'w', encoding='utf8') as f:
            yaml.dump(config.dict(), f)
        return

    with open(CONFIG_FILE_PATH, 'r', encoding='utf8') as f:
        config_data = yaml.load(f)

    config = Config(**config_data)
    updated = False

    # 添加缺失的字段并更新注释
    new_config_data = config.dict()
    for key, value in Config().dict().items():
        if key not in config_data:
            new_config_data[key] = value
            updated = True

    if updated:
        with open(CONFIG_FILE_PATH, 'w', encoding='utf8') as f:
            yaml.dump(new_config_data, f)
        return
    return config


def add_yaml_comments():
    with open(CONFIG_FILE_PATH, 'r', encoding='utf8') as f:
        config_data = yaml.load(f)

    for field in Config.__fields__.values():
        if field.field_info.description:
            config_data.yaml_add_eol_comment(field.field_info.description, field.name)

    with open(CONFIG_FILE_PATH, 'w', encoding='utf8') as f:
        yaml.dump(config_data, f)


def get_config() -> Optional[Config]:
    result = load_or_create_config()
    add_yaml_comments()
    return result
