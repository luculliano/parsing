"""scrap full https://parsinger.ru/"""

import asyncio
import re
from typing import Iterator

import aiohttp
from bs4 import BeautifulSoup


URL_SOURCE = "https://parsinger.ru/html/index1_page_1.html"
URL_TEMPLATE = "https://parsinger.ru/html/"
URL_PAGEN = "https://parsinger.ru/html/index{category}_page{page}.html"


async def get_markup(url: str) -> str:
    """it's used to extract html markup from url"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text("utf-8")


async def get_category_links(url_source: str) -> Iterator[str]:
    """
    it's used to extract categories links from source url.
    forms iterator of categories urls based on URL_TEMPLATE
    """
    markup = await get_markup(url_source)
    soup = BeautifulSoup(markup, "lxml")
    return (
        f"{URL_TEMPLATE}{i['href']}"
        for i in soup.find("div", class_="nav_menu").find_all("a")
    )


async def get_pagen_links(url_category: str) -> Iterator[str]:
    """
    it's used to extract all pagination links from category url
    forms iterator of pages urls based on URL_TEMPLATE
    """
    markup = await get_markup(url_category)
    soup = BeautifulSoup(markup, "lxml")
    return (
        f"{URL_TEMPLATE}{i['href']}"
        for i in soup.find("div", class_="pagen").find_all("a")
    )


async def get_card_links(url_page: str) -> Iterator[str]:
    """
    it's used to extract all cards links from page url
    forms iterator of cards urls based on URL_TEMPLATE
    """
    markup = await get_markup(url_page)
    soup = BeautifulSoup(markup, "lxml")
    return (
        f"{URL_TEMPLATE}{div.find('a')['href']}"
        for div in soup.find_all("div", class_="sale_button")
    )


async def get_good_revenue(url_card: str) -> int:
    """it's used to extract revenue number from card url"""
    markup = await get_markup(url_card)
    soup = BeautifulSoup(markup, "lxml")
    price = int(soup.find("span", id="price").text.split()[0])
    amount = int(soup.find("span", id="in_stock").text.split()[2])
    return price * amount


async def main() -> None:
    for url_category in await get_category_links(URL_SOURCE):
        for url_page in await get_pagen_links(url_category):
            for url_card in await get_card_links(url_page):
                print(url_card)



if __name__ == "__main__":
    asyncio.run(main())
