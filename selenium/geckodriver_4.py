"""using multiprocessing"""
from pathlib import Path
from time import sleep
import re
from fake_useragent import FakeUserAgent
from selenium import webdriver
from multiprocessing import Pool

urls = "https://time.com/", "https://www.wsj.com/", "https://www.nbcnews.com/"


def setup_driver() -> webdriver.FirefoxOptions:
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", FakeUserAgent().random)
    return options


def main(url: str) -> None:
    options = setup_driver()
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        driver.get_screenshot_as_file(Path(__file__).parent.joinpath(
                    re.sub(r"\.", "_", re.sub(r"https://|/", "", url)) + ".png"))
        sleep(5)


if __name__ == "__main__":
    pool = Pool(3)
    pool.map(main, urls)
