import asyncio
import csv
from typing import Iterable
from faker import Faker
from secrets import randbelow
from time import monotonic
import time


###############################################################################
# async calling principle, it will be different output depending on the function
# that is faster
# without tasks it would not be the increment in uptime, because funcs are called
# one by one
# async def one(num: int = 1) -> None:
#     time = randbelow(6)
#     await asyncio.sleep(time)
#     print(f"{one.__name__} coroutine with arg {num} and {time} sec sleep")


# async def two(num: int = 2) -> None:
#     time = randbelow(6)
#     await asyncio.sleep(time)
#     print(f"{two.__name__} coroutine with arg {num} and {time} sec sleep")


# async def main() -> None:
#     task1 = asyncio.create_task(one())
#     task2 = asyncio.create_task(two())
#     start = monotonic()
#     await task1
#     await task2
#     # await one()
#     # await two()
#     print("Programm uptime =", monotonic() - start)


# asyncio.run(main())

###############################################################################
# with gather function
# async def one(num: int = 1) -> None:
#     time = randbelow(6)
#     await asyncio.sleep(time)
#     print(f"{one.__name__} coroutine with arg {num} and {time} sec sleep")


# async def two(num: int = 2) -> None:
#     time = randbelow(6)
#     await asyncio.sleep(time)
#     print(f"{two.__name__} coroutine with arg {num} and {time} sec sleep")


# async def main() -> None:
#     start = monotonic()
#     for _ in range(5):
#         await asyncio.gather(one(), two())
#         print("---")
#     print("Programm uptime =", monotonic() - start)


# asyncio.run(main())
###############################################################################
# make tasks as a iterable. It is like one func gather all pages from one site
# async def one(num: int) -> None:
#     time = randbelow(6)
#     await asyncio.sleep(time)
#     print(f"Number = {num} with time {time} sec")

# async def main() -> None:
#     tasks = (asyncio.create_task(one(i)) for i in range(1, 11))
#     start = monotonic()
#     await asyncio.gather(*tasks)
#     print(monotonic() - start)


# asyncio.run(main())
###############################################################################
# these three funcs gather pages from 3 different sites
# gather func can get a Future object as argument so use this:
# i use wait not gather, no difference, only try.
# async def one(num: int) -> None:
#     await asyncio.sleep(randbelow(6))
#     print("Number =", num)


# async def two(num: int) -> None:
#     await asyncio.sleep(randbelow(6))
#     print("Number =", num)


# async def three(num: int) -> None:
#     await asyncio.sleep(randbelow(6))
#     print("Number =", num)


# async def main() -> None:
#     group1 = asyncio.gather(*(one(i) for i in range(1, 11)))
#     group2 = asyncio.gather(*(two(i) for i in range(1, 11)))
#     group3 = asyncio.gather(*(three(i) for i in range(1, 11)))
#     start = monotonic()
#     await asyncio.wait((group1, group2, group3))
#     print(monotonic() - start)


# asyncio.run(main())
###############################################################################
# IO-bound operations: sleep as get query and write in csv
faker = Faker("ru_RU")


async def make_user(uid: int) -> dict[str, str | int]:
    """Функция создает словарь, значения которого будут переданы
    в объект DictWriter и записаны в файл
    """
    await asyncio.sleep(1)
    return {"id_user": uid, "name": faker.name(), "email": faker.email()}


async def main() -> None:
    tasks = (asyncio.create_task(make_user(i)) for i in range(1, 11))
    with open("users.csv", "w", encoding="utf-8") as file:
        headings = "id_user", "name", "email"
        writer = csv.DictWriter(file, headings)
        start = monotonic()
        writer.writerows(await asyncio.gather(*tasks))
        print(f"Uptime = {monotonic() - start} sec")


if __name__ == "__main__":
    asyncio.run(main())
###############################################################################
