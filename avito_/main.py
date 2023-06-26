import functools
import itertools
import json
import logging
from pathlib import Path
import pickle
import re
import sys
from time import monotonic, sleep
from typing import Iterable, Iterator

from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import requests

pagens = 1
domain = "https://www.avito.ru"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    datefmt="%d.%m.%Y, %H:%M:%S",
)


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as err:
            logging.error(err)
    return wrapper


def prepare_pagens(n: int) -> Iterable[str]:
    """returns all pagen links with each session"""
    url_pagen = "https://www.avito.ru/perm/avtomobili?cd=1&p={page}&radius=200&searchRadius=200"
    return (url_pagen.format(page=i) for i in range(1, n + 1))


def save_markup(markup: str, file_name: str) -> None:
    with open(file_name, "w") as file:
        file.write(markup)
        logging.info("markup saved")


def save_json(card_data: dict[str, str]) -> None:
    with open(Path(__file__).parent.joinpath("avito_cars.json"), "a",
              encoding="utf-8") as file:
        json.dump(card_data, file, ensure_ascii=False, indent=3)
        logging.info("append car data in json file")


@error_handler
def get_card(session: requests.Session, url: str) -> str:
    markup = session.get(url, headers=headers, timeout=10).content.decode()
    return markup


@error_handler
def get_card_data(session: requests.Session, url: str) -> str:
    markup = session.get(url, headers=headers, timeout=10).content.decode()
    return markup


def parse_pagen(markup_pagen: str) -> Iterable[str]:
    soup = BeautifulSoup(markup_pagen, "lxml")
    card_urls = [
    f'{domain}{card.find("div", class_="iva-item-title-py3i_").find("a")["href"]}'
    for card in soup.find_all("div", class_="iva-item-body-KLUuy")
    ]
    logging.info("grab all car links from pagen") if card_urls else \
                logging.info("grab all car links from pagen FAILED")
    return card_urls


@error_handler
def get_pagen(session: requests.Session, pagen_url: str) -> Iterable[str]:
    """returns all card's url from pagen as 2 threads"""
    markup_pagen = session.get(pagen_url, headers=headers, timeout=10).content.decode()
    return parse_pagen(markup_pagen)


def parse_card_data(markup_card_data: str) -> dict[str, str]:
    """parse additional data from characteritics url page"""
    soup = BeautifulSoup(markup_card_data, "lxml")
    cols = ("Расход топлива смешанный", "Разгон до 100 км/ч",
            "Колея передняя", "Колея задняя", "Длина", "Высота",
            "Дорожный просвет", "Ёмкость топливного бака")
    full = {k.text: v.text for i in soup.find_all("div", class_="desktop-1jb7eb2")
            for k, v in [i.find_all("span")]}
    return dict(filter(lambda tpl: tpl[0] in cols, full))


@error_handler
def parse_card(session: requests.Session, markup_card: str) -> None:
    """total card parsing"""
    soup = BeautifulSoup(markup_card, "lxml")
    card_data_url = domain + \
        soup.find("div", class_="params-specification-__5qD").find("a")["href"]  # pyright: ignore
    card_data_markup = get_card_data(session, card_data_url)
    addons = parse_card_data(card_data_markup)
    title = soup.find("span", class_="title-info-title-text").text  # pyright: ignore
    brand, model = title.split()[0], title.split()[1].strip(",")
    date = soup.find("span", {"data-marker": "item-view/item-date"})
    price = soup.find("span", {"class": "styles-module-size_m-Co_QG", "itemprop": "price"})
    loc = soup.find("span", class_="style-item-address__string-wt61A")
    data = {i[0]: i[1] for i in map(lambda x: re.split(r": ", x),
            (i.text for i in soup.find("ul", class_="params-paramsList-zLpAu")))}  # pyright: ignore
    addons.update(dict(title=title, brand=brand, model=model,
                       date=date.text.strip("· ") if date else "",
                       price=price.text if price else "",
                       loc=loc.text if loc else ""))
    data.update(addons)
    save_json(data)


def get_proxy() -> Iterator[dict[str, str] | None]:
    with open("proxies.pql", "rb") as file:
        return itertools.cycle(pickle.load(file))


if __name__ == "__main__":
    start = monotonic()
    proxies = get_proxy()
    for pagen_url in prepare_pagens(pagens):
        headers = {"user-agent": FakeUserAgent().random}
        proxy = next(proxies)
        session = requests.Session()
        for card_url in get_pagen(session, pagen_url):
            # headers = {"user-agent": FakeUserAgent().random}
            # proxy = next(proxies)
            markup_card = get_card(session, card_url)
            parse_card(session, markup_card)
            sleep(2)
        session.close()
    print(monotonic() - start)
