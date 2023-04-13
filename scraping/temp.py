import asyncio
import csv
from faker import Faker
from time import monotonic

# import time

faker = Faker("ru_RU")


async def make_user(uid: int) -> dict[str, str | int]:
    """Корутина, имитирующая выполнение какой-либо операции
    и создающая словарь, значения которого будут переданы
    в объект DictWriter и записаны в файл
    """
    await asyncio.sleep(1)
    return {"id_user": uid, "name": faker.name(), "email": faker.email()}


async def main() -> None:
    tasks = (asyncio.create_task(make_user(i)) for i in range(1, 1001))
    with open("users.csv", "w", encoding="utf-8") as file:
        headings = "id_user", "name", "email"
        writer = csv.DictWriter(file, headings)
        start = monotonic()
        writer.writerows(await asyncio.gather(*tasks))
        print(f"Uptime = {monotonic() - start} sec")


if __name__ == "__main__":
    asyncio.run(main())

# faker = Faker("ru_RU")


# def make_user(uid: int) -> dict[str, str | int]:
    # """Функция, имитирующая выполнение какой-либо операции
    # и создающая словарь, значения которого будут переданы
    # в объект DictWriter и записаны в файл
    # """
#     time.sleep(1)
#     return {"id_user": uid, "name": faker.name(), "email": faker.email()}


# def main() -> None:
#     tasks = (make_user(i) for i in range(1, 11))
#     with open("users.csv", "w", encoding="utf-8") as file:
#         headings = "id_user", "name", "email"
#         writer = csv.DictWriter(file, headings)
#         start = monotonic()
#         writer.writerows(tasks)
#         print(f"Uptime = {monotonic() - start} sec")


# if __name__ == "__main__":
#     main()
