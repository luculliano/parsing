import asyncio
from time import monotonic

from arsenic import browsers, get_session, services

GECKODRIVER = "geckodriver"

async def open_link(session, url):
    await session.get(url)


async def process_links(links):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        tasks = [asyncio.create_task(open_link(session, url)) for url in links]
        await asyncio.gather(*tasks)


links = [
    'https://www.google.com',
    'https://www.example.com',
    'https://www.facebook.com',
    'https://www.amazon.com',
    'https://www.wikipedia.org',
    'https://www.twitter.com',
    'https://www.linkedin.com',
    'https://www.nytimes.com',
    'https://www.reddit.com',
]

start = monotonic()
asyncio.run(process_links(links))
print(monotonic() - start)
