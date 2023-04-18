"""cpu bound no difference"""
import asyncio
from time import monotonic

TOTAL = 100


async def cpu_bound_func() -> None:
    count = 0
    start = monotonic()
    for _ in range(50_000):
        count += 1

    print(f"uptime = {monotonic() - start} sec")


async def main() -> None:
    start = monotonic()
    tasks = asyncio.gather(*(cpu_bound_func() for _ in range(TOTAL)))
    await asyncio.gather(tasks)
    # tasks = (asyncio.create_task(cpu_bound_func()) for _ in range(TOTAL))
    # await asyncio.gather(*tasks)

    print(f"Final async programm uptime = {monotonic() - start} sec")


def scpu_bound_func() -> None:
    count = 0
    start = monotonic()
    for _ in range(50_000):
        count += 1

    print(f"uptime = {monotonic() - start} sec")


def smain() -> None:
    start = monotonic()
    for _ in range(TOTAL):
        scpu_bound_func()

    print(f"Final sync programm uptime = {monotonic() - start} sec")


if __name__ == "__main__":
    asyncio.run(main())
    smain()
