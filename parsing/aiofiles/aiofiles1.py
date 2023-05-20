"""comparison of reading one file, for many files the same result
async is slower than sync"""

import asyncio
from time import monotonic

import aiofiles


async def async_main() -> None:
    async with aiofiles.open("file_1.txt") as file:
        start = monotonic()
        async for _ in file:
            pass
        print(async_main.__name__, monotonic() - start)


def sync_main() -> None:
    with open("file_1.txt") as file:
        start = monotonic()
        for _ in file:
            pass
        print(sync_main.__name__, monotonic() - start)


if __name__ == "__main__":
    sync_main()
    asyncio.run(async_main())
