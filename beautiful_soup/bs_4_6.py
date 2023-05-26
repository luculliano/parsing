from bs4 import BeautifulSoup
from requests import get


url = "https://parsinger.ru/table/1/index.html"


def save_table_data() -> None:
    with get(url) as response:
        markup = response.content.decode()
        with open("table.html", "w") as file:
            file.write(markup)


def sum_nums_in_table() -> float:
    """sum of all numbers in table"""
    with open("table.html") as file:
        soup = BeautifulSoup(file.read(), "lxml")
        return sum(float(i.text) for i in soup.find_all("td"))


if __name__ == "__main__":
    print(sum_nums_in_table())
