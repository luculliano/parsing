import requests
from fake_useragent import FakeUserAgent

url_page = "https://rezka.ag/films/crime/1237-lico-so-shramom-1983.html"
url = "https://httpbin.org/cookies"

headers = {"user-agent": FakeUserAgent().random}


def get_cookies(url: str) -> None:
    response = requests.get(url, headers=headers)
    jar = response.cookies
    print(jar.list_paths(), jar.list_domains())


def pass_cookies(url: str, cookies: dict[str, str]) -> None:
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.text)


if __name__ == "__main__":
    get_cookies(url_page)
