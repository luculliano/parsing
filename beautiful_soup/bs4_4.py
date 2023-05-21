import re
from typing import Iterable

from bs4 import BeautifulSoup
from requests import get

URL = "https://parsinger.ru/html/index3_page_1.html"
TEMPLATE_PAGES = "https://parsinger.ru/html/"
TEMPLATE_CARDS = TEMPLATE_PAGES


def get_html(path: str) -> str:
    with get(path) as res:
        return res.content.decode()


def parse_pagens(url: str, template: str) -> Iterable[str]:
    """Parse all pagination links"""
    markup = get_html(url)
    soup = BeautifulSoup(markup, "lxml")
    urls = (
        f"{template}{x['href']}" for x in soup.find("div", class_="pagen").find_all("a")
    )
    return urls


def parse_cards(urls: Iterable[str], template: str) -> list[Iterable[str]]:
    """parse all good's cards links on pages"""
    cards = []
    for url in urls:
        markup = get_html(url)
        soup = BeautifulSoup(markup, "lxml")
        links = (
            f"{template}{card.find('a')['href']}"
            for card in soup.find_all("div", class_="sale_button")
        )
        cards.append(links)
    return cards


def parse_articles(links: list[Iterable[str]]) -> int:
    articles = []
    for page in links:
        for link in page:
            markup = get_html(link)
            soup = BeautifulSoup(markup, "lxml")
            article = int(
                re.search(r"\d+", soup.find("p", class_="article").text).group()
            )
            articles.append(article)
    return sum(articles)


if __name__ == "__main__":
    urls = parse_pagens(URL, TEMPLATE_PAGES)
    links = parse_cards(urls, TEMPLATE_CARDS)
    print(parse_articles(links))
