import asyncio
from ctypes import resize
import json
from time import monotonic

import aiofiles
import aiohttp

###############################################################################
# simple get query
# async def main() -> None:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(
#             "https://api.covidtracking.com/v1/us/current.json"
#         ) as response:
#             text = await response.json()
#             print(json.dumps(*text, indent=2))


# asyncio.run(main())
###############################################################################
# using proxy
# async def main() -> None:
#     headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"}
#     proxy = "http://72bb24:ed1aea@87.251.76.222:1010"
#     # proxy_auth = aiohttp.BasicAuth(login="72bb24", password="ed1aea")
#     async with aiohttp.ClientSession() as session:
#         async with session.get("https://ipinfo.io/json",
#                                proxy=proxy,
#                                # proxy_auth=proxy_auth
#                                headers=headers) as response:
#             print(await response.text())


# asyncio.run(main())
###############################################################################
# without context manager
# async def main() -> str:
#     session = aiohttp.ClientSession()
#     response = await session.get("https://httpbin.org/user-agent")
#     await session.close()
#     return await response.text()
# print(asyncio.run(main()))
###############################################################################
# read file with aiofiles.open function
# async def main() -> None:
#     async with aiofiles.open("proxies.txt", encoding="utf-8") as file:
#         print(await file.read())


# asyncio.run(main())
###############################################################################
