import asyncio
from pathlib import Path
import aiofiles
from time import monotonic
import requests
import aiohttp
from bs4 import BeautifulSoup

###############################################################################
# comparison, it is the same for many files
# async def async_main() -> None:
#     async with aiofiles.open("file_1.txt") as file:
#         start = monotonic()
#         async for _ in file:
#             pass
#         print(async_main.__name__, monotonic() - start)


# def sync_main() -> None:
#     with open("file_1.txt") as file:
#         start = monotonic()
#         for _ in file:
#             pass
#         print(sync_main.__name__, monotonic() - start)

# # sync is faster than async
# asyncio.run(async_main())
# sync_main()
###############################################################################
# download file = 74.76 sec;  sync = 94.22 sec
# url = "https://parsinger.ru/asyncio/aiofile/1/video/nu_pogodi.mp4"
# async def main() -> None:
#     start = monotonic()
#     async with aiofiles.open("video.mp4", "wb") as file:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 async for chunk in response.content.iter_chunked(100_000):
#                     await file.write(chunk)
#         print(monotonic() - start)
# asyncio.run(main())
#
# url = "https://parsinger.ru/asyncio/aiofile/1/video/nu_pogodi.mp4"
# def main() -> None:
#     start = monotonic()
#     with open("video.mp4", "wb") as file:
#         with requests.get(url) as response:
#             for chunk in response.iter_content(100_000):
#                 file.write(chunk)
#         print(monotonic() - start)
# main()
###############################################################################
# download a lot of pictures, async = 12.50 sec, sync = 73.22
# url = "https://parsinger.ru/asyncio/aiofile/1/index.html"
# path = Path("images")

# async def write_file(filename: str, url: str, session: aiohttp.ClientSession) -> None:
#     async with aiofiles.open(path.joinpath(filename), "wb") as file:
#         async with session.get(url) as response:
#             async for chunk in response.content.iter_chunked(1024):
#                 await file.write(chunk)
#         print(filename)

# async def main() -> None:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             soup = BeautifulSoup(await response.text(), "lxml")
#             imgs_urls = (f"https://parsinger.ru/asyncio/aiofile/1/{img['src']}" for img in soup.find_all("img"))
#             # tasks = (asyncio.create_task(write_file(Path(img_url).name, img_url, session) for img_url in imgs_urls))
#             tasks = asyncio.gather(*(write_file(Path(img_url).name, img_url, session) for img_url in imgs_urls))
#             await asyncio.gather(tasks)
# start = monotonic()
# asyncio.run(main())
# print(monotonic() - start)
#
# def main() -> None:
#     with requests.get(url) as response:
#         soup = BeautifulSoup(response.text, "lxml")
#         imgs_urls = (f"https://parsinger.ru/asyncio/aiofile/1/{img['src']}" for img in soup.find_all("img"))

#     for img_url in imgs_urls:
#         filename = Path(img_url).name
#         with open(path.joinpath(filename), "wb") as file:
#             with requests.get(url) as response:
#                 for chunk in response.iter_content(1024):
#                     file.write(chunk)
#         print(filename)


# start = monotonic()
# main()
# print(monotonic() - start)
###############################################################################
