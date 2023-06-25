import asyncio
from time import monotonic

from arsenic import browsers, get_session, services, Session, keys, session

GECKODRIVER = "geckodriver"

async def click_checkbox(session: Session, n: int) -> None:
    checkbox = await session.wait_for_element(1, f"input.check:nth-child({n})")
    await checkbox.click()


async def main() -> None:
    """click on checkbox"""
    url = "https://parsinger.ru/selenium/4/4.html"
    async with get_session(services.Geckodriver(binary=GECKODRIVER), browsers.Firefox()) as session:
        await session.get(url)
        tasks = (asyncio.create_task(click_checkbox(session, i)) for i in range(1, 521))
        await asyncio.gather(*tasks)


start = monotonic()
asyncio.run(main())
print(monotonic() - start)
