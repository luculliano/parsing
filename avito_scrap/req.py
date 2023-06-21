import json
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import requests
from tqdm import tqdm

# URL = "https://www.avito.ru/perm/avtomobili?cd=1&p={page}&radius=200&searchRadius=200"
URL = "https://www.avito.ru/all/avtomobili/land_rover"
domain = "https://www.avito.ru"
headers = {"user-agent": FakeUserAgent().random}
data = []

logging.basicConfig(filename="avito_cars.log",
                    filemode="a", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s", force=False)


async def get_response_aioh(session: ClientSession) -> None:
    """returns 403 with unknown reason"""
    async with session.get(URL, headers=headers) as res:
        print(res.status, res.url, res.request_info)


def get_page(url: str, page: int) -> str:
    res = requests.get(url.format(page=page), headers=headers, timeout=5)
    return res.content.decode()


def save_json(data: list[dict]) -> None:
    with open("avito_cars.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    logging.info("json file saved!")


def parse_page(markup: str) -> None:
    soup = BeautifulSoup(markup, "lxml")
    for item in soup.find_all("div", class_="iva-item-body-KLUuy"):
        car = item.find("div", class_="iva-item-title-py3i_").find("a")
        details = (item.find("div", class_="iva-item-autoParamsStep-WzfS8").text
                   if item.find("div", class_="iva-item-autoParamsStep-WzfS8")
                   is not None else None)
        price = (item.find("div", class_="price-price-JP7qe").text
                 if item.find("div", class_="price-price-JP7qe") is not None
                 else None)
        description = (item.find("div", class_="iva-item-descriptionStep-C0ty1").text
                       if item.find("div", class_="iva-item-descriptionStep-C0ty1")
                       is not None else None)
        seller = (item.find("span", class_="iva-item-text-Ge6dR iva-item-hideWide-_C9JT").text
                  if item.find("span", class_="iva-item-text-Ge6dR iva-item-hideWide-_C9JT")
                  is not None else None)
        place = (item.find("div", class_="geo-root-zPwRk").text if
                 item.find("div", class_="geo-root-zPwRk").text is not None
                 else None)
        car_info = dict(name=car.text, url=f"{domain}{car['href']}",
                        details=details, price=price, seller=seller,
                        place=place, description=description)
        data.append(car_info)


def main() -> None:
    for i in tqdm(range(3)):
        try:
            markup = get_page(URL, i)
            parse_page(markup)
        except requests.ConnectionError as err:
            logging.error(err)
            continue
    if data: save_json(data)


if __name__ == "__main__":
    main()
