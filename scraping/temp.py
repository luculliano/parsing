import asyncio
from time import monotonic

import aiofiles
import aiohttp
import requests


# check proxies in file
async def main() -> None:
    proxy = "http://72bb24:ed1aea@87.251.76.222:1010"
    async with aiofiles.open("proxies.txt", encoding="utf-8") as file:
        start = monotonic()
        for _ in await file.readlines():
            # proxy = f"http://{line.strip()}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://httpbin.org/ip",
                                           proxy=proxy, timeout=5) as response:
                        print(response.status)
            except Exception:
                continue
    print("uptime =", monotonic() - start)


# asyncio.run(main())

#headers = {
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
#}
def main2() -> None:
    with open("proxies.txt", encoding="utf-8") as file:
        proxy = {"https": "https://72bb24:ed1aea@87.251.76.222:1010",
                 "http": "https://72bb24:ed1aea@87.251.76.222:1010"}
        start = monotonic()
        for _ in file:
            # proxy = dict(http=line.strip(), https=line.strip())
            try:
                with requests.get("https://httpbin.org/ip",
                                  timeout=5) as response:
                    print(response.status_code)
            except Exception as err:
                print(err)
    print("uptime =", monotonic() - start)
main2()
