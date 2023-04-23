from aiogram import Bot
from dotenv import load_dotenv
import os
import logging
import asyncio

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(TOKEN)

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    await bot.send_message("6112169873", "qwerty123")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
