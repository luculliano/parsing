from datetime import datetime
from secrets import choice
from typing import NamedTuple
from zoneinfo import ZoneInfo

import aiohttp


class Fact(NamedTuple):
    event: str
    year: int


async def get_random_fact() -> Fact:
    """function to get random fact for current date"""

    async with aiohttp.ClientSession() as session:
        dt = datetime.now(ZoneInfo("Europe/Moscow"))
        url = f"https://api.api-ninjas.com/v1/historicalevents"
        params = {"day": dt.day, "month": dt.month, "offset": -1}
        headers = {"X-Api-Key": "CUQfcoHQEax80S+oA5/w2Q==aagceJEVKl9QIeWI"}
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()
            fact = await _parse_fact(choice(data))
            return fact


async def _parse_fact(data: dict[str, str]) -> Fact:
    """function to parse fact"""
    event, year = data["event"], int(data["year"])
    return Fact(event=event, year=year)
