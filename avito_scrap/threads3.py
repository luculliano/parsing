import threading
from time import sleep

from fake_useragent import FakeUserAgent
from selenium.webdriver import Firefox, FirefoxOptions

URL = "https://httpbin.org/ip", "https://httpbin.org/headers"
headers = {"user-agent": FakeUserAgent().random}


def configure_driver() -> FirefoxOptions:
    options = FirefoxOptions()
    options.set_preference("general.useragent.override", headers["user-agent"])
    # options.add_argument("--headless")
    return options


def main(i: int) -> None:
    options = configure_driver()
    with Firefox(options=options) as driver:
        driver.get(URL[i])
        print(driver.current_url)
        sleep(5)


if __name__ == "__main__":
    a = (threading.Thread(target=main, args=(i,)) for i in range(2))
    for i in a:
        i.start()
