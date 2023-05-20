import re

from bs4 import BeautifulSoup
from requests import get


def get_html(path: str) -> str:
    with get(path) as res:
        return res.content.decode()


def parse_html() -> None:
    """Print total sum of items on page"""
    markup = get_html("https://parsinger.ru/html/index1_page_1.html")
    soup = BeautifulSoup(markup, "lxml")
    prices = (x.text for x in soup.find_all("p", class_="price"))
    prices = (re.search(r"\d+", x).group() for x in prices)
    total = sum(float(x) for x in prices)
    print(total)


if __name__ == "__main__":
    parse_html()
