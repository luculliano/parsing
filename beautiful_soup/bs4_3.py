from pprint import pprint
from typing import Iterable

from bs4 import BeautifulSoup
from requests import get

URL = "https://parsinger.ru/html/index1_page_1.html"
TEMPLATE_1 = "https://parsinger.ru/html/"
TEMPLATE_2 = "https://parsinger.ru/html/index1_page_{page}.html"


def get_html(path: str) -> str:
    with get(path) as res:
        return res.content.decode()


def parse_last_page(url: str) -> int:
    """
    Parse last pagination page to give it
    in loop for generating urls via f-string
    """
    markup = get_html(url)
    soup = BeautifulSoup(markup, "lxml")
    last_page = soup.find("div", class_="pagen").find_all("a")[-1].text
    return int(last_page)


def generate_urls(template: str) -> Iterable[str]:
    last_page = parse_last_page(URL)
    return (template.format(page=i) for i in range(1, last_page + 1))


def parse_links(url: str, template: str) -> Iterable[str]:
    """Parse all pagination links"""
    markup = get_html(url)
    soup = BeautifulSoup(markup, "lxml")
    urls = (f"{template}{x['href']}" for x in
            soup.find("div", class_="pagen").find_all("a"))
    return urls


def parse_names(urls: Iterable[str]) -> dict[int, tuple[str]]:
    d = {}
    for index, page in enumerate(urls, start=1):
        markup = get_html(page)
        soup = BeautifulSoup(markup, "lxml")
        d.setdefault(index, tuple(x.text for x in soup.find_all("a", class_="name_item")))
    return d


if __name__ == "__main__":
    urls = parse_links(URL, TEMPLATE_1)
    pprint(parse_names(urls))
