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
    cookies_path: str = Field(default='cookies.json', description="cookies文件路径，第一次运行会生成，一般无需修改")
    greeting: str = Field(default='嗨嗨嗨', description="直播间开播时发送的弹幕")
    bark_key: str = Field(default=None, description="Bark App的Key，用于推送消息")
    bark_icon: str = Field(default=None, description="Bark App的Icon，用于推送消息")
    debug: bool = Field(default=False, description="是否开启调试模式")


CONFIG_FILE_PATH = 'config.yaml'
yaml = YAML()


def load_or_create_config() -> Optional[Config]:
    if not os.path.exists(CONFIG_FILE_PATH):
        config = Config()
        with open(CONFIG_FILE_PATH, 'w', encoding='utf8') as f:
            yaml.dump(config.model_dump(), f)
        return

    with open(CONFIG_FILE_PATH, 'r', encoding='utf8') as f:
        config_data = yaml.load(f)

    config = Config(**config_data)
    updated = False

    # 添加缺失的字段并更新注释
    new_config_data = config.model_dump()
    for key, value in Config().model_dump().items():
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

    for field_name, field in Config.model_fields.items():
        if field.description:
            config_data.yaml_add_eol_comment(field.description, field_name)

    with open(CONFIG_FILE_PATH, 'w', encoding='utf8') as f:
        yaml.dump(config_data, f)


def get_config() -> Optional[Config]:
    result = load_or_create_config()
    add_yaml_comments()
    return result


ConfigObj = get_config()

if not ConfigObj:
    print('配置文件需要手动填写。请修改 config.yaml 文件。')
    exit(1)
else:
    print('读取配置文件成功')
    # 打印每个字段的名称和值以及描述
    for field_name, field_info in Config.model_fields.items():
        value = getattr(ConfigObj, field_name)
        description = field_info.description
        if isinstance(value, bool):
            value = '是' if value else '否'
        print(f"{description}: {value} ")