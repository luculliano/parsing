"""auth forms via cookies not work so use profiles (create it in first in about:profiles)"""
import json
from os import getenv
from time import sleep

from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://stepik.org/learn"

login = getenv("SK_LOGIN")
password = getenv("SK_PASS")


def save_cookies(cookies: list[dict]) -> None:
    with open("cookies.json", "w", encoding="utf-8") as file:
        json.dump(cookies, file)


def read_cookies() -> list[dict]:
    with open("cookies.json", encoding="utf-8") as file:
        return json.load(file)


def setup_driver() -> webdriver.FirefoxOptions:
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", FakeUserAgent().random)
    options.add_argument("-profile")
    options.add_argument("/home/luculliano/.mozilla/firefox/8t0o2jpq.dev")
    return options


def auth_to_server(driver: webdriver.Firefox) -> None:
    login_input = driver.find_element(By.NAME, "login")
    login_input.clear()
    login_input.send_keys(login)

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(password)

    driver.find_element(By.CSS_SELECTOR, ".sign-form__btn").click()


def main(url: str) -> None:
    options = setup_driver()
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        sleep(5)
        driver.refresh()
        sleep(5)


if __name__ == "__main__":
    main(url)
