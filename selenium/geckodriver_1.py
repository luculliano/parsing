"""using proxy and check ip"""
import csv
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

csv_file = "./good_proxies.csv"
url = "https://whoer.net/"


def get_proxies(csv_file: str) -> list[str]:
    with open(csv_file, encoding="utf-8") as file:
        content = csv.DictReader(file)
        return [f"{i['ip_address']}:{i['port']}" for i in content]


def get_query(url: str, proxy: str) -> None:
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    # capabilities["marionette"] = True
    capabilities["proxy"] = {"proxyType": "MANUAL", "httpProxy": proxy, "sslProxy": proxy}
    with webdriver.Firefox(proxy=proxy) as browser:
        browser.get(url)
        result = browser.find_element(By.TAG_NAME, "strong").text
        browser.set_page_load_timeout(5)
        print(result)
        sleep(5)


if __name__ == "__main__":
    proxy = get_proxies(csv_file)[0]
    get_query(url, proxy)
