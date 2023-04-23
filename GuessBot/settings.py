import asyncio
import logging.config
import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()


class TelegramBotHandler(logging.Handler):
    def __init__(self, token: str, chat_id: str) -> None:
        super().__init__()
        self._token, self._chat_id = token, chat_id

    async def log(self, record: logging.LogRecord) -> None:
        bot = Bot(self._token)
        await bot.send_message(self._chat_id, self.format(record))
        await bot.session.close()

    def emit(self, record: logging.LogRecord) -> None:
        asyncio.run(self.log(record))


LOGGING_CONFIG = {
    "version": 1,  # for compataability if ithis config will change in future only
    "disable_existing_loggers": False,  # not disable existing loggers
    # specify formatters
    "formatters": {
        "default_formatter": {"format": "[%(levelname)s:%(asctime)s] %(message)s"},
    },
    # specify handlers
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "telegram_handler": {
            "class": "__main__.TelegramBotHandler",
            "formatter": "default_formatter",
            "token": os.getenv("BOT_TOKEN", ""),
            "chat_id": "6112169873",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default_formatter",
            "filename": "first-log.log",
            "maxBytes": 20,
            "backupCount": 3,
        },
    },
    # specify loggers
    "loggers": {
        "first_logger": {
            "handlers": ["telegram_handler", "stream_handler"],
            "level": "INFO",
            "propagate": True,  # let inheritation
        }
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("first_logger")
logger.info("let's check the output")
