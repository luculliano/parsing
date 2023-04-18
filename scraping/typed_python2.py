import asyncio
from typing import Any, NamedTuple, TypeAlias

import aiohttp
import os

TOKEN = os.getenv("OWM_TOKEN")

Celcius: TypeAlias = float


class Coordinates(NamedTuple):
    longitude: float
    latitude: float


class Weather(NamedTuple):
    temperature: Celcius
    city: str
    weather_type: str


class CantGetCoordinates(Exception):
    """Program can't get current coordinates"""


class ApiServiceError(Exception):
    """Program can't get current weather"""


async def _parse_coordinates() -> Coordinates:
    ip_data = await _get_ip_data()
    loc = map(float, ip_data["loc"].split(","))
    return Coordinates(*loc)


async def _get_ip_data() -> dict[str, str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ipinfo.io/json", timeout=10) as response:
                return await response.json()
    except Exception:
        raise CantGetCoordinates


async def _get_openweather_data() -> dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as session:
            lat, lon = await _parse_coordinates()
            params = {"appid": TOKEN, "lat": lat, "lon": lon, "units": "metric"}
            async with session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params=params,
                timeout=30,
            ) as response:
                return await response.json()
    except Exception:
        raise ApiServiceError


async def _parse_weather() -> Weather:
    weather_data = await _get_openweather_data()
    temperature = weather_data["main"]["temp"]
    city = weather_data["name"]
    weather_type = weather_data["weather"][0]["description"]
    return Weather(temperature, city, weather_type)


async def get_weather() -> None:
    temp, city, weather_type = await _parse_weather()
    print(f"{city}: {temp}°C, {weather_type}")


async def main() -> None:
    task = asyncio.create_task(get_weather())
    await asyncio.gather(task)


if __name__ == "__main__":
    asyncio.run(main())
