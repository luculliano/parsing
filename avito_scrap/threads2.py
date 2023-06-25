import json
import threading

from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import requests

URL = "https://www.avito.ru/all/avtomobili/land_rover?p={page}"
domain = "https://www.avito.ru"
headers = {"user-agent": FakeUserAgent().random}


def get_page(url: str, page: int) -> str:
    res = requests.get(url.format(page=page), headers=headers, timeout=5)
    return res.content.decode()


def save_json(data: dict) -> None:
    with open("avito_cars.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def parse_page(url: str, page: int) -> None:
    markup = get_page(url, page)
    soup = BeautifulSoup(markup, "lxml")
    for item in soup.find_all("div", class_="iva-item-body-KLUuy"):
        car = item.find("div", class_="iva-item-title-py3i_").find("a")
        details = (
            item.find("div", class_="iva-item-autoParamsStep-WzfS8").text
            if item.find("div", class_="iva-item-autoParamsStep-WzfS8") is not None
            else None
        )
        price = (
            item.find("div", class_="price-price-JP7qe").text
            if item.find("div", class_="price-price-JP7qe") is not None
            else None
        )
        description = (
            item.find("div", class_="iva-item-descriptionStep-C0ty1").text
            if item.find("div", class_="iva-item-descriptionStep-C0ty1") is not None
            else None
        )
        seller = (
            item.find("span", class_="iva-item-text-Ge6dR iva-item-hideWide-_C9JT").text
            if item.find("span", class_="iva-item-text-Ge6dR iva-item-hideWide-_C9JT")
            is not None
            else None
        )
        place = (
            item.find("div", class_="geo-root-zPwRk").text
            if item.find("div", class_="geo-root-zPwRk").text is not None
            else None
        )
        car_info = dict(
            name=car.text,
            url=f"{domain}{car['href']}",
            details=details,
            price=price,
            seller=seller,
            place=place,
            description=description,
        )
        save_json(car_info)


def main() -> None:
    thrds = (threading.Thread(target=parse_page, args=(URL, i)) for i in range(1, 11))
    for thrd in thrds:
        thrd.start()


if __name__ == "__main__":
    main()
