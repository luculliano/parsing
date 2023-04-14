import asyncio
from time import monotonic

import aiofiles
import aiohttp
import requests


# check proxies in file
async def main() -> None:
    async with aiofiles.open("proxies.txt", encoding="utf-8") as file:
        start = monotonic()
        for index, line in enumerate(await file.readlines(), start=1):
            proxy = f"http://{line.strip()}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://httpbin.org/ip", proxy=proxy, timeout=5
                    ) as response:
                        print(index, response.status, proxy)
            except Exception:
                continue
    print("uptime =", monotonic() - start)


asyncio.run(main())

#####
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
}
with open("proxies.txt", encoding="utf-8") as file:
    start = monotonic()
    for line in file:
        proxy = dict(http=line.strip(), https=line.strip())
        try:
            with requests.get(
                "https://httpbin.org/ip", proxies=proxy, headers=headers, timeout=5
            ) as response:
                print(response.text)
        except Exception as err:
            continue
    print("uptime =", monotonic() - start)
