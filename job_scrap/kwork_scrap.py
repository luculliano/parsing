import asyncio

from aiohttp import ClientSession
from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup

url = "https://kwork.ru/projects?c=41"

headers = {"user-agent": FakeUserAgent().random}


async def get_query(session: ClientSession, url: str):
    async with session.get(url, timeout=5, headers=headers) as response:
        return response.request_info.headers
        # markup = await response.text(encoding="utf-8")
        # soup = BeautifulSoup(markup, "lxml")
        # return soup
    # with open("/home/luculliano/Downloads/kwork.html") as file:
    #     soup = BeautifulSoup(file.read(), "lxml")
    #     links = (i.find("a").text for i in soup.find_all("div", class_="wants-card__header-title first-letter breakwords pr250"))
    #     return list(links)


async def main() -> None:
    async with ClientSession() as session:
        response = await get_query(session, url)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
