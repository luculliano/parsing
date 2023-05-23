"""scrap full https://parsinger.ru/"""

import asyncio
from time import monotonic
from typing import Iterator

from aiohttp import ClientSession
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

URL = "https://parsinger.ru/html/index1_page_1.html"
DOMAIN = "https://parsinger.ru/html/"


def get_category_links(url_source: str) -> Iterator[str]:
    """it extracts all category links from source url, firstly"""
    response = requests.get(url_source)
    soup = BeautifulSoup(response.content.decode(), "lxml")
    return (f"{DOMAIN}{i['href']}"
            for i in soup.find("div", class_="nav_menu").find_all("a"))


async def get_pagen_links(url_category: str, session: ClientSession) -> Iterator[str]:
    """it extracts all pagination links from category url, secondly"""
    async with session.get(url_category) as response:
        soup = BeautifulSoup(await response.text(encoding="utf-8"), "lxml")
        return (f"{DOMAIN}{i['href']}"
                for i in soup.find("div", class_="pagen").find_all("a"))


async def grab_pagen_links(session: ClientSession) -> Iterator[str]:
    """grabs all pagen links to use them to extract card links, thirdly"""
    tasks = [asyncio.create_task(get_pagen_links(i, session))
             for i in get_category_links(URL)]
    result = [await f for f in tqdm(asyncio.as_completed(tasks),
                            total=len(tasks), ascii=True, desc="grabbing pages...")]
    return (j for i in result for j in i)


async def get_card_links(url_page: str, session: ClientSession) -> Iterator[str]:
    """it extracts all cards links from page url, fourthly"""
    async with session.get(url_page) as response:
        soup = BeautifulSoup(await response.text(encoding="utf-8"), "lxml")
        return (f"{DOMAIN}{div.find('a')['href']}"
                for div in soup.find_all("div", class_="sale_button"))


async def grab_card_links(session: ClientSession) -> Iterator[str]:
    """grabs all card links to use them to extract card info, fifthly"""
    urls_page = await grab_pagen_links(session)
    tasks = [asyncio.create_task(get_card_links(i, session)) for i in urls_page]
    result = [await f for f in tqdm(asyncio.as_completed(tasks),
                            total=len(tasks), ascii=True, desc="grabbing cards...")]
    return (j for i in result for j in i)


async def get_good_revenue(url_card: str, session: ClientSession) -> int:
    """it extracts revenue number from card url, sixthly"""
    async with session.get(url_card) as response:
        soup = BeautifulSoup(await response.text("utf-8"), "lxml")
        price = int(soup.find("span", id="price").text.split()[0])
        amount = int(soup.find("span", id="in_stock").text.split()[2])
        return price * amount


async def get_cards_info(session: ClientSession) -> str:
    """it combines each card result as last step"""
    urls_card = await grab_card_links(session)
    tasks = [asyncio.create_task(get_good_revenue(i, session)) for i in urls_card]
    result = [await f for f in tqdm(asyncio.as_completed(tasks),
                            total=len(tasks), ascii=True, desc="summarizing...")]
    return f"result: {sum(result)} rub"


async def main() -> None:
    start = monotonic()
    async with ClientSession() as session:
        print(await get_cards_info(session))
    print("total uptime:", monotonic() - start)


if __name__ == "__main__":
    asyncio.run(main())
