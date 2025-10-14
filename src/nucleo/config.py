from pydantic import BaseModel as BaseSection
from pydantic_settings import BaseSettings


class AppSettings(BaseSection):
    NAME: str = "nucleo"
    DEBUG: bool = False


class TelegramBot(BaseSection):
    BOT_TOKEN: str
    WEBHOOK_SECRET: str
    MACROBOT_HOST: str


class Settings(BaseSettings):
    APP: AppSettings
    TELEGRAM: TelegramBot

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
