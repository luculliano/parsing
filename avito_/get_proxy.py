"""parse free http proxies"""

import asyncio
import csv
from pathlib import Path
from typing import Iterable

from aiohttp import ClientSession
from bs4 import BeautifulSoup

url = "https://hidemy.name/en/proxy-list/?type=hs#list"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "*/*",
    "Cookie": "PAPVisitorId=ce0fa373f1707c712284b04150YymZei; PAPVisitorId=ce0fa373f1707c712284b04150YymZei; _ga_KJFZ3PJZP3=GS1.1.1685167039.1.1.1685167177.0.0.0; _ga=GA1.1.706526997.1685167039; _ym_uid=1685167039560618683; _ym_d=1685167039; _ym_isad=1; _ym_hostIndex=0-3%2C1-0; cf_chl_2=a7375133ae2842b; cf_clearance=wq3rvVLx1FCWKy9seRoMRNOhTp1XXjhriEOy5XsS5sQ-1685167097-0-150",
}

columns = ("ip_address", "port", "country_city",
           "speed", "type", "anonymity", "latest_update")


async def get_page_proxies(url_page: str, session: ClientSession) -> Iterable[dict]:
    """parses all table rows with proxies as iterable of dicts"""
    async with session.get(url_page) as response:
        soup = BeautifulSoup(await response.text("utf-8"), "lxml")
        rows = soup.find("div", class_="table_block").find("tbody").find_all("tr")
        proxies = (dict(zip(columns, (j.text for j in i.find_all("td")))) for i in rows)
        return proxies


def save_data_to_csv(proxies: Iterable[dict]) -> None:
    with open(Path(__file__).parent.joinpath("proxies.csv"),
              "w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, columns, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(proxies)


def get_pagen_links(end: int) -> Iterable[str]:
    """generates pagen links from 2 page to 252, each page has 64 proxies"""
    template = "https://hidemy.name//en/proxy-list/?type=hs&start={n}#list"
    return (template.format(n=i) for i in range(64, end, 64))


async def main() -> None:
    async with ClientSession(headers=headers) as session:
        task = asyncio.create_task(get_page_proxies(url, session))
        tasks = (asyncio.create_task(get_page_proxies(i, session))
                 for i in get_pagen_links(640))
        proxies = (j for i in await asyncio.gather(task, *tasks) for j in i)
        save_data_to_csv(proxies)


if __name__ == "__main__":
    asyncio.run(main())
