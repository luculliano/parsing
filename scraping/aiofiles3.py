"""download a lot of pictures
async = 12.50 sec, sync = 73.22"""

import asyncio
from pathlib import Path
from time import monotonic

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup

url = "https://parsinger.ru/asyncio/aiofile/1/index.html"
path = Path("images")


async def write_file(filename: str, url: str, session: aiohttp.ClientSession) -> None:
    async with aiofiles.open(path.joinpath(filename), "wb") as file:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                await file.write(chunk)
        print(filename)


async def async_main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            imgs_urls = (
                f"https://parsinger.ru/asyncio/aiofile/1/{img['src']}"
                for img in soup.find_all("img")
            )
            tasks = asyncio.gather(
                *(
                    write_file(Path(img_url).name, img_url, session)
                    for img_url in imgs_urls
                )
            )
            await asyncio.gather(tasks)


def sync_main() -> None:
    with requests.get(url) as response:
        soup = BeautifulSoup(response.text, "lxml")
        imgs_urls = (
            f"https://parsinger.ru/asyncio/aiofile/1/{img['src']}"
            for img in soup.find_all("img")
        )
    for img_url in imgs_urls:
        filename = Path(img_url).name
        with open(path.joinpath(filename), "wb") as file:
            with requests.get(url) as response:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        print(filename)


if __name__ == "__main__":
    start = monotonic()
    sync_main()
    print(monotonic() - start)

    start = monotonic()
    asyncio.run(async_main())
    print(monotonic() - start)
