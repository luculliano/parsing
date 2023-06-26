import functools
import logging
import re
import sys
import threading
from time import monotonic
from typing import Iterable

from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import requests
from requests.adapters import HTTPAdapter

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


@error_handler
def get_card(session: requests.Session, url: str) -> str:
    markup = session.get(url, headers=headers, timeout=4).content.decode()
    return markup


@error_handler
def get_card_data(session: requests.Session, url: str) -> str:
    markup = session.get(url, headers=headers, timeout=4).content.decode()
    return markup


def get_markup_file(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()


def parse_pagen(markup_pagen: str) -> tuple[list[str], list[str]]:
    soup = BeautifulSoup(markup_pagen, "lxml")
    card_urls = [
    f'{domain}{card.find("div", class_="iva-item-title-py3i_").find("a")["href"]}'
    for card in soup.find_all("div", class_="iva-item-body-KLUuy")
    ]
    logging.info("grab all car links from pagen") if card_urls else \
                logging.info("grab all car links from pagen FAILED")
    thread1, thread2 = (
            card_urls[:round(len(card_urls) / 2)],
            card_urls[round(len(card_urls) / 2):]
    )
    return thread1, thread2


@error_handler
def get_pagen(session: requests.Session, pagen_url: str) -> tuple[list[str], list[str]]:
    """returns all card's url from pagen as 2 threads"""
    markup_pagen = session.get(pagen_url, headers=headers, timeout=4).content.decode()
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


def parse_card(session: requests.Session, card_url: str) -> dict:
    """total card parsing"""
    markup_card = get_card(session, card_url)
    soup = BeautifulSoup(markup_card, "lxml")
    card_data_url = domain + \
        soup.find("div", class_="params-specification-__5qD").find("a")["href"]  # pyright: ignore
    addons = parse_card_data(get_card_data(session, card_data_url))
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
    logging.info("parsed full car's data")
    return print(data)


def make_threads() -> tuple[list[threading.Thread], list[threading.Thread]]:
    threads = get_pagen(session, pagen_markup)
    threads1, threads2 = (
        [threading.Thread(target=parse_card, args=(session, card_url))
         for card_url in threads[0]],
        [threading.Thread(target=parse_card, args=(session, card_url))
         for card_url in threads[1]]
    )
    return threads1, threads2


def start_threads(threads1: list[threading.Thread],
                  threads2: list[threading.Thread]) -> None:
    for thread in threads1:
        thread.start()
    for thread in threads1:
        thread.join()
    logging.info("finish half pagen")
    for thread in threads2:
        thread.start()
    for thread in threads2:
        thread.join()
    logging.info("finish full pagen")


if __name__ == "__main__":
    start = monotonic()
    for pagen_markup in prepare_pagens(1):
        headers = {"user-agent": FakeUserAgent().random}
        session = requests.Session()
        session.mount("https://", HTTPAdapter(20, 20))
        threads1, threads2 = make_threads()
        start_threads(threads1, threads2)
        session.close()
    print(monotonic() - start)
