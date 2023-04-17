"""bot that sends pictures"""
from typing import Any
import aiohttp
import asyncio
import os
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(funcName)s",
    stream=sys.stdout,
    datefmt="%d.%m.%Y, %H:%M:%S",
)


class PictureBot:
    async def __init__(self) -> None:
        self.__TOKEN = os.getenv("TOKEN_BOT")

    async def _get_picture(self) -> str:
        """get picture from third-party api"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search"
            ) as response:
                logging.info("")
                result = await response.json()
                return result[0]["url"]


    async def getUpdates(self, offset: int) -> dict[Any, Any] | None:
        url = f"https://api.telegram.org/bot{self.__TOKEN}/getUpdates"
        params = {"offset": offset + 1}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                updates = await response.json()
                logging.info("get updates")
                try:
                    return updates["result"][0]
                except IndexError:
                    return None


    async def _parseUpdates(self, result: dict[Any, Any]) -> tuple[int, int]:
        offset = result["update_id"]
        chat_id = result["message"]["from"]["id"]
        return offset, chat_id


    async def sendPhoto(self, chat_id: int, photo_link: str) -> None:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        params = {"chat_id": chat_id, "photo": photo_link}
        async with aiohttp.ClientSession() as session:
            await session.get(url, params=params)
            logging.info("send photo")


async def main() -> None:
    bot = PictureBot()
    offset = -2
    while True:
        updates = await bot.getUpdates(offset)
        if updates is not None:
            offset, chat_id = await bot._parseUpdates(updates)
            photo = await bot._get_picture()
            await bot.sendPhoto(chat_id, photo)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
