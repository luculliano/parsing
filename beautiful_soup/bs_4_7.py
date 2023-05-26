from functools import reduce
from operator import add

from bs4 import BeautifulSoup
from requests import get


def get_table_data_0() -> float:
    """sum of all numbers in first column"""
    url = "https://parsinger.ru/table/2/index.html"
    response = get(url).content.decode()
    soup = BeautifulSoup(response, "lxml")
    return sum(float(i.find("td").text)
               for i in soup.find("table").find_all("tr")
               if i.find("td") is not None)


def get_table_data_1() -> float:
    """sum of all numbers in table that are bold"""
    url = "https://parsinger.ru/table/3/index.html"
    response = get(url).content.decode()
    soup = BeautifulSoup(response, "lxml")
    return sum(float(i.find("b").text)
               for i in soup.find_all("td") if i.find("b") is not None)


def get_table_data_2() -> float:
    """sum of all numbers in table that are in green cell"""
    url = "https://parsinger.ru/table/4/index.html"
    response = get(url).content.decode()
    soup = BeautifulSoup(response, "lxml")
    return sum(float(i.text) for i in soup.find_all("td", class_="green"))


def get_table_data_3() -> float:
    """sum of all rows like orange*blue in table"""
    url = "https://parsinger.ru/table/5/index.html"
    response = get(url).content.decode()
    soup = BeautifulSoup(response, "lxml")
    blues = (float(i.text) for i in soup.select("td:last-child"))
    oranges = (float(i.text) for i in soup.find_all("td", class_="orange"))
    return reduce(add, reduce(add, zip(oranges, blues)))


def get_table_data_4() -> dict[str, float]:
    """sum of all rows like orange*blue in table"""
    url = "https://parsinger.ru/table/5/index.html"
    response = get(url).content.decode()
    soup = BeautifulSoup(response, "lxml")
    d = {}
    headers = (i.text for i in soup.find_all("th"))
    rows = [i.find_all("td") for i in soup.find_all("tr")][1:]
    for index, col in enumerate(headers):
        d.setdefault(col, round(sum(float(i[index].text) for i in rows), 3))
    return d


if __name__ == "__main__":
    print(get_table_data_4())
