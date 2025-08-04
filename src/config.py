from typing import Optional

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


# 定义配置模型
class Config(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls, toml_file="config.toml"),
            file_secret_settings,
        )

    room_id: int = Field(default=6846214, description="直播间ID")
    target_gift_id: int = Field(
        default=31036, description="要送的礼物ID（默认是小花花）"
    )
    target_gift_num: int = Field(default=1, description="要送的礼物数量")
    delay: int = Field(default=60, description="送礼物延时（秒）")
    greeting: Optional[str] = Field(default=None, description="直播间开播时发送的弹幕")
    bark_key: Optional[str] = Field(
        default=None, description="Bark App的Key，用于推送消息"
    )
    bark_icon: Optional[str] = Field(
        default=None, description="Bark App的Icon，用于推送消息"
    )
    cookie_cloud_url: str = Field(..., description="CookieCloud URL")
    cookie_cloud_uuid: str = Field(..., description="CookieCloud UUID")
    cookie_cloud_password: str = Field(..., description="CookieCloud Password")


# 创建全局配置实例
setting = Config()
