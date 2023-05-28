"""auth forms via selenium"""
from os import getenv
from time import sleep

from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "https://rutracker.org/forum/index.php"

login = getenv("RT_LOGIN")
password = getenv("RT_PASS")


def get_query(url: str) -> None:
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", FakeUserAgent().random)
    with webdriver.Firefox(options=options) as browser:
        browser.get(url)

        browser.find_element(By.LINK_TEXT, "Вход").click()

        login_input = browser.find_element(By.ID, "top-login-uname")
        login_input.clear()
        login_input.send_keys(login)

        password_input = browser.find_element(By.ID, "top-login-pwd")
        password_input.clear()
        password_input.send_keys(password)

        browser.find_element(By.NAME, "login").send_keys(Keys.ENTER)

        sleep(5)


if __name__ == "__main__":
    get_query(url)
