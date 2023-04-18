import asyncio
from typing import NamedTuple

import aiohttp


class Coordinates(NamedTuple):
    longitude: float
    latitude: float


async def _parse_coordinates() -> Coordinates:
    result = await get_coordinates()
    loc = map(float, result["loc"].split(","))
    return Coordinates(*loc)


async def get_coordinates() -> dict[str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ipinfo.io/json") as response:
            return await response.json()


async def main() -> None:
    task = asyncio.create_task(_parse_coordinates())
    result = await asyncio.gather(task)
    coordinates = result[0]
    print(coordinates.longitude, coordinates.latitude, sep="\n")


if __name__ == "__main__":
    asyncio.run(main())
