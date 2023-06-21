"""
https://www.avito.ru/perm/transport
https://www.avito.ru/all/transport
Подгружает рекомендации, работают динамически, можно исп. selenium

URL = "https://www.avito.ru/perm/avtomobili?cd=1&p=1&radius=200&searchRadius=200"
Реализуется пагинация, можно исп. requests, aiohhtp не работает.
"""

from time import sleep

from fake_useragent import FakeUserAgent
from selenium.webdriver import Firefox, FirefoxOptions

URL = "https://www.whatismybrowser.com/detect/what-is-my-user-agent/"
headers = {"user-agent": FakeUserAgent().random}


def configure_driver() -> FirefoxOptions:
    options = FirefoxOptions()
    options.set_preference("general.useragent.override", headers["user-agent"])
    # options.add_argument("--headless")
    return options


def save_source(driver: Firefox) -> None:
    with open("source_code2.html", "w") as file:
        file.write(driver.page_source)


def main() -> None:
    options = configure_driver()
    with Firefox(options=options) as driver:
        driver.get(URL)
        save_source(driver)
        sleep(2)


if __name__ == "__main__":
    main()
