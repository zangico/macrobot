import asyncio
import logging

from nucleo import settings
from telegram.bot import TelegramBot

host = settings.API.HOST
port = settings.API.PORT

### GUNICORN CONFIGURATION
bind = f"{host}:{port}"
workers = settings.API.WORKERS
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 5
timeout = 30
loglevel = "debug" if settings.APP.DEBUG else "info"


class SuppressWinchFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:
            return True
        return not (msg.startswith("Handling signal:") and "winch" in msg.lower())


logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "format": (
                "[%(asctime)s,%(msecs)03d][%(process)d][%(levelname)s][gc:control] "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "format": (
                "[%(asctime)s,%(msecs)03d][%(process)d][%(levelname)s][gc:api] "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "suppress_winch": {
            "()": SuppressWinchFilter,
        },
    },
    "handlers": {
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stderr",
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": "ext://sys.stdout",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "filters": ["suppress_winch"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


def on_starting(server):

    async def startup():
        await bot.set_webhook()

    TOKEN = settings.TELEGRAM.BOT_TOKEN
    SECRET = settings.TELEGRAM.WEBHOOK_SECRET
    HOST = settings.TELEGRAM.MACROBOT_HOST

    if not TOKEN or not SECRET or not HOST:
        server.log.warning(
            "Telegram env vars not fully set, skipping webhook registration."
        )
        return

    bot = TelegramBot(TOKEN, SECRET, HOST)
    try:
        asyncio.run(startup())
        server.log.info("Telegram webhook registered by master process.")
    except Exception as e:
        server.log.error(f"Error registering Telegram webhook: {e}")
