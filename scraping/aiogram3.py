"""guess historical event
learn: use ram, ssd for communication
- generate number 0-100
- conditions: in game, out game
- count attemts
- compare answers with number

"""
import asyncio
from datetime import date, datetime
from aiogram import Bot, Dispatcher
import os
import logging
from aiogram.types.message import Message
from aiogram.filters import Command
import aiohttp
from zoneinfo import ZoneInfo
from secrets import choice
from typing import NamedTuple
import re

TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


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


@dp.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        'Hey! Let\'s play a game of "Guess the Date"?\n\n'
        "To get the rules of the game and a list of available "
        "commands, send the command /help."
    )


@dp.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(
        '"Guess the Date" game rules:\n\nI give you a historical event, '
        "and you have to tell me what year it happened.\n\n"
        "Example answers: 1998 or -10\n\n"
        "Available commands:\n"
        "/play - to start playing\n"
        "/gup - to give up\n"
        "/cancel - to cancel game\n"
        "/stat - to show stat\n"
        "/help - rules of the game and list of teams\n\n"
        "Let's start now? Just send /play"
    )


data: dict = {
    "in_game": False,
    "event_year": None,
    "attempts": 5,
    "total_games": 0,
    "wins": 0,
}


@dp.message(Command("play"))
async def proceed_play(message: Message) -> None:
    if data["in_game"] == True:
        await message.reply("You are in game. Send number instead.")
    else:
        fact = await get_random_fact()
        await message.reply(fact.event)
        data["in_game"] = True
        data["event_year"] = fact.year


@dp.message(lambda x: x.text and re.fullmatch(r"[-+]?\d*", x.text))
async def proceed_numbers(message: Message) -> None:
    if data["in_game"] == False:
        await message.reply("You are not in game yet. Send /play to start.")
    else:
        if data["attempts"] < 2:
            await message.reply(
                f"You lose! Answer is {data['event_year']}. Send /play to start again."
            )
            data["attempts"] = 5
            data["in_game"] = False
            data["total_games"] += 1
            return
        usr_year = int(message.text)
        if usr_year == data["event_year"]:
            await message.reply(f"That's right!")
            data["attempts"] = 5
            data["in_game"] = False
            data["total_games"] += 1
            data["wins"] += 1
            return
        elif usr_year > data["event_year"]:
            data["attempts"] -= 1
            await message.reply(f"Too much. Attempts left: {data['attempts']}")
        elif usr_year < data["event_year"]:
            data["attempts"] -= 1
            await message.reply(f"Too low. Attempts left: {data['attempts']}")


@dp.message(Command("cancel"))
async def proceed_cancel(message: Message) -> None:
    if data["in_game"] == True:
        await message.reply("Current game cancelled")
        data["attempts"] = 5
        data["in_game"] = False
        data["total_games"] += 1
    else:
        await message.reply("Not in game - so no to cancel")


@dp.message(Command("stat"))
async def proceed_stat(message: Message) -> None:
    await message.reply(
        f"Statistic\n\n"
        f"Games: {data['total_games']}\n"
        f"Wins: {data['wins']}"
    )


async def _parse_fact(data: dict[str, str]) -> Fact:
    """function to parse fact"""
    event, year = data["event"], int(data["year"])
    return Fact(event=event, year=year)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
