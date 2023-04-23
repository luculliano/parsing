import asyncio
import logging
import os
from typing import Sequence

from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types.message import Message
from dotenv import load_dotenv

admin_ids = 13123, 1241241, 1412432, 36554645, 6112169873
admin_cmds = "/real", "/xxx", "/xyz"

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class OnlyAdmins(BaseFilter):
    def __init__(self, admin_ids: Sequence[int], admin_cmds: Sequence[str]) -> None:
        self.admin_ids = admin_ids
        self.admin_cmds = admin_cmds

    async def __call__(self, message: Message) -> bool | dict:
        return (
            message.from_user.id in self.admin_ids  # pyright: ignore
            and message.text in self.admin_cmds
        )


@dp.message(OnlyAdmins(admin_ids, admin_cmds))
async def admin_reply(message: Message) -> None:
    await message.reply("Admin")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
