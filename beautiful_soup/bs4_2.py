import re

from bs4 import BeautifulSoup
from requests import get


def get_html(path: str) -> str:
    with get(path) as res:
        return res.content.decode()


def parse_html() -> None:
    """Calculate sale"""
    markup = get_html("https://parsinger.ru/html/hdd/4/4_1.html")
    soup = BeautifulSoup(markup, "lxml")
    cur_price = float(re.search(r"\d+", soup.find("span", id="price").text).group())
    old_price = float(re.search(r"\d+", soup.find("span", id="old_price").text).group())
    print("Sale:", round(100 - (cur_price / old_price * 100), 1), "%")

if __name__ == "__main__":
    parse_html()
