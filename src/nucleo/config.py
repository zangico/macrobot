from pydantic import BaseModel as BaseSection
from pydantic_settings import BaseSettings


class AppSettings(BaseSection):
    NAME: str = "orbita-app"
    DEBUG: bool = False
    SEND_ERROR: bool = False

class ApiSettings(BaseSection):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 4

class TelegramBot(BaseSection):
    BOT_TOKEN: str
    WEBHOOK_SECRET: str
    MACROBOT_HOST: str
    SEND_ERROR: bool = False
    ADMIN_CHAT_ID: int


class Settings(BaseSettings):
    APP: AppSettings
    API: ApiSettings
    TELEGRAM: TelegramBot
    MACRODROID_WEBHOOK: str

    class Config:
        env_nested_delimiter = "__"
        extra = "allow"


settings = Settings()
