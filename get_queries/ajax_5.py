"""auth using post method to hacker news. See what are in the post request data first"""
import csv
import json
from os import getenv
from random import choice

from fake_useragent import FakeUserAgent
import requests
from requests.cookies import RequestsCookieJar

domain = "https://news.ycombinator.com/login"
url = "https://httpbin.org/ip"

headers = {"user-agent": FakeUserAgent().random}

data = {
    "acct": getenv("HN_ACCT"),
    "pw": getenv("HN_PW")
    # "creating": "t",  # to register, but it's captcha
}


def get_proxy() -> dict[str, str]:
    # with open("good_proxies.csv") as file:
    #     content = choice(list(csv.DictReader(file)))
    #     proxy = f"http://{content['ip_address']}:{content['port']}"
    proxy = "5.78.73.221:8080"
    return dict(http=proxy, https=proxy)


def save_cookies(cookies):
    with open("cookies.json", "w", encoding="utf-8") as file:
        json.dump(cookies, file)


def get_query(url: str) -> None:
    with requests.Session() as session:
        response = session.post(url, headers=headers, proxies=get_proxy(),
                                timeout=5, data=data, params={"goto": "news"})
        print(response.status_code)


if __name__ == "__main__":
    get_query(domain)
