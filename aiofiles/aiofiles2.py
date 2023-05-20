"""download large files
async = 74.76 sec, sync = 94.22
"""
import asyncio
from time import monotonic

import aiofiles
import aiohttp
import requests

url = "https://parsinger.ru/asyncio/aiofile/1/video/nu_pogodi.mp4"


async def async_main() -> None:
    start = monotonic()
    async with aiofiles.open("video.mp4", "wb") as file:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                async for chunk in response.content.iter_chunked(100_000):
                    await file.write(chunk)
        print(monotonic() - start)


def sync_main() -> None:
    start = monotonic()
    with open("video.mp4", "wb") as file:
        with requests.get(url) as response:
            for chunk in response.iter_content(100_000):
                file.write(chunk)
        print(monotonic() - start)


if __name__ == "__main__":
    sync_main()
    asyncio.run(async_main())
