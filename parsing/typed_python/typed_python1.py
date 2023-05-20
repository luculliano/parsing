from enum import Enum
from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple

from pympler.asizeof import asizeof


##############################################################################
# dataclass
@dataclass
class Coordinates:
    longitude: float
    latitude: float


def get_coordinates() -> Coordinates:
    return Coordinates(10, 20)


coordinates = get_coordinates()

a, b = coordinates.longitude, coordinates.latitude


print(asizeof(coordinates))  # 344

##############################################################################
# ENUM

Celcius = int


class WeatherType(Enum):
    RAIN = "Дождь"
    THUNDER = "Гроза"


class Weather(NamedTuple):
    # weather_type: str
    weather_type: WeatherType
    sun: bool
    temperature: Celcius


def get_weather() -> Weather:
    return Weather(weather_type=WeatherType.RAIN, sun=True, temperature=21)


print(get_weather().weather_type.value)
print(WeatherType.THUNDER.name)


##############################################################################
# NamedTuple
class Coordinates2(NamedTuple):
    longitude: float
    latitude: float


def get_coordinates2() -> Coordinates2:
    return Coordinates2(12, 33)


coordinates = get_coordinates2()

print(asizeof(coordinates))  # 120

Coordinates4 = namedtuple("Coordinates4", "longitude,latitude")
coordinates = Coordinates4(12, 44)
print(asizeof(coordinates))  # 120
