import asyncio
import csv
import logging
from secrets import randbelow
from time import monotonic

from faker import Faker


###############################################################################
# async calling principle, it will be different output depending on the function
# that is faster
# without tasks it would not be the increment in uptime, because funcs are called
# one by one
async def one1(num: int = 1) -> None:
    time = randbelow(6)
    await asyncio.sleep(time)
    print(f"{one1.__name__} coroutine with arg {num} and {time} sec sleep")


async def two1(num: int = 2) -> None:
    time = randbelow(6)
    await asyncio.sleep(time)
    print(f"{two1.__name__} coroutine with arg {num} and {time} sec sleep")


async def main1() -> None:
    task1 = asyncio.create_task(one1())
    task2 = asyncio.create_task(two1())
    start = monotonic()
    await task1
    await task2
    # await one()
    # await two()
    print("Programm uptime =", monotonic() - start)


asyncio.run(main1())


###############################################################################
# with gather function
async def one2(num: int = 1) -> None:
    time = randbelow(6)
    await asyncio.sleep(time)
    print(f"{one2.__name__} coroutine with arg {num} and {time} sec sleep")


async def two2(num: int = 2) -> None:
    time = randbelow(6)
    await asyncio.sleep(time)
    print(f"{two2.__name__} coroutine with arg {num} and {time} sec sleep")


async def main2() -> None:
    start = monotonic()
    for _ in range(5):
        await asyncio.gather(one2(), two2())
        print("---")
    print("Programm uptime =", monotonic() - start)


asyncio.run(main2())


###############################################################################
# make tasks as a iterable. It is like one func gather all pages from one site
async def one3(num: int) -> None:
    time = randbelow(6)
    await asyncio.sleep(time)
    print(f"Number = {num} with time {time} sec")


async def main3() -> None:
    tasks = (asyncio.create_task(one3(i)) for i in range(1, 11))
    start = monotonic()
    await asyncio.gather(*tasks)
    print(monotonic() - start)


asyncio.run(main3())


###############################################################################
# these three funcs gather pages from 3 different sites
# gather func can get a Future object as argument so use this:
# i use wait not gather, no difference, only try.
async def one4(num: int) -> None:
    await asyncio.sleep(randbelow(6))
    print("Number =", num)


async def two4(num: int) -> None:
    await asyncio.sleep(randbelow(6))
    print("Number =", num)


async def three4(num: int) -> None:
    await asyncio.sleep(randbelow(6))
    print("Number =", num)


async def main4() -> None:
    group1 = asyncio.gather(*(one4(i) for i in range(1, 11)))
    group2 = asyncio.gather(*(two4(i) for i in range(1, 11)))
    group3 = asyncio.gather(*(three4(i) for i in range(1, 11)))
    start = monotonic()
    await asyncio.wait((group1, group2, group3))
    print(monotonic() - start)


asyncio.run(main4())
###############################################################################
# IO-bound operations: sleep as get query and write in csv + logging
faker = Faker("ru_RU")


logging.basicConfig(
    filename="first_log.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)


async def make_user(uid: int) -> dict[str, str | int]:
    await asyncio.sleep(1)
    return {"id_user": uid, "name": faker.name(), "email": faker.email()}


async def main5() -> None:
    tasks = (asyncio.create_task(make_user(i)) for i in range(1, 11))
    with open("users.csv", "w", encoding="utf-8") as file:
        headings = "id_user", "name", "email"
        writer = csv.DictWriter(file, headings)
        start = monotonic()
        writer.writerows(await asyncio.gather(*tasks))
        print(f"Uptime = {monotonic() - start} sec")
    logging.info("generate lines")


if __name__ == "__main__":
    asyncio.run(main5())
###############################################################################
