from selenium.webdriver import Firefox, FirefoxOptions
from time import monotonic

GECKODRIVER = "geckodriver"


def process_links(links: list[str]):
    with Firefox() as session:
        for i in links:
            session.get(i)


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
process_links(links)
print(monotonic() - start)
