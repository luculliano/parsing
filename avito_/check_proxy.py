"""check is proxy alive saving them in good_proxies.csv"""

import asyncio
from pathlib import Path
from typing import Iterable
import csv
from aiohttp import ClientSession

url = "https://httpbin.org/ip"
csv_file = "../good_proxies.csv"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
}

columns = ("ip_address", "port", "country_city",
           "speed", "type", "anonymity", "latest_update")


def get_proxies(csv_file: str) -> tuple[dict[str, str]]:
    with open(csv_file, encoding="utf-8") as file:
        content = csv.DictReader(file)
        return tuple(content)


def save_data_to_csv(proxies: Iterable[dict]) -> None:
    with open(Path(__file__).parent.joinpath("good_proxies.csv"),
              "w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, columns, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(proxies)


async def check_proxy(url: str, session: ClientSession,
                      proxy: dict[str, str]) -> dict[str, str] | None:
    proxy_value = f"{proxy['ip_address']}:{proxy['port']}"
    try:
        async with session.get(url, proxy=f"http://{proxy_value}",
                               timeout=5) as response:
            if response.status == 200:
                return proxy
    except Exception:
        pass


async def main() -> None:
    async with ClientSession(headers=headers) as session:
        proxies = get_proxies(csv_file)
        tasks = (asyncio.create_task(check_proxy(url, session, i)) for i in proxies)
        result = (i for i in await asyncio.gather(*tasks) if i)
        save_data_to_csv(result)


if __name__ == "__main__":
    asyncio.run(main())
