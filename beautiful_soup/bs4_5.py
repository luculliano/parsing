"""scrap full https://parsinger.ru/"""

# add progres bar
# decrease uptime
# add dataa to csv to make analysis

import asyncio
from time import monotonic
from typing import Iterator

import aiohttp
from bs4 import BeautifulSoup
import requests


URL = "https://parsinger.ru/html/index1_page_1.html"
DOMAIN = "https://parsinger.ru/html/"


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content.decode(), "lxml")


def get_category_links(url: str) -> Iterator[str]:
    """it's used to extract all category links from source url"""
    soup = get_soup(url)
    return (
        f"{DOMAIN}{i['href']}"
        for i in soup.find("div", class_="nav_menu").find_all("a")
    )


def get_pagen_links(url: str) -> Iterator[str]:
    """it's used to extract all pagination links from category url"""
    soup = get_soup(url)
    return (
        f"{DOMAIN}{i['href']}"
        for i in soup.find("div", class_="pagen").find_all("a")
    )


def get_card_links(url: str) -> Iterator[str]:
    """it's used to extract all cards links from page url"""
    soup = get_soup(url)
    return (
        f"{DOMAIN}{div.find('a')['href']}"
        for div in soup.find_all("div", class_="sale_button")
    )


def grab_all_links() -> Iterator[str]:
    urls_category = get_category_links(URL)
    urls_page = (get_pagen_links(i) for i in urls_category)
    urls_card = (get_card_links(j) for i in urls_page for j in i)
    return (j for i in urls_card for j in i)


async def get_good_revenue(url: str, session: aiohttp.ClientSession) -> int:
    """it's used to extract revenue number from card url"""
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text("utf-8"), "lxml")
        price = int(soup.find("span", id="price").text.split()[0])
        amount = int(soup.find("span", id="in_stock").text.split()[2])
        return price * amount


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        tasks = (asyncio.create_task(get_good_revenue(i, session)) for i in grab_all_links())
        revenue = await asyncio.gather(*tasks)
        print("total revenue value:", sum(revenue), "rub")


if __name__ == "__main__":
    start = monotonic()
    asyncio.run(main())
    print("total uptime:", monotonic() - start)
