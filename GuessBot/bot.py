import asyncio
from aiogram import Bot, Dispatcher
import os
import logging
from aiogram.types.message import Message
from aiogram.filters import Command
import re
from facts import get_random_fact

TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

users: dict = {}


@dp.message(Command("start"))
async def proceed_start(message: Message) -> None:
    await message.answer(
        'Hey! Let\'s play a game of "Guess the Date"?\n\n'
        "To get the rules of the game and a list of available "
        "commands, send the command /help."
    )

    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "in_game": False,
            "total_games": 0,
            "attempts": 5,
            "wins": 0,
            "event_year": None,
        }


@dp.message(Command("help"))
async def proceed_help(message: Message) -> None:
    await message.answer(
        '"Guess the Date" game rules:\n\nI give you a historical event'
        "that happend this day, "
        "and you have to tell me what year it happened.\n\n"
        "Example answers: 1998 or -10\n\n"
        "Available commands:\n"
        "/play - to start playing\n"
        "/gup - to give up\n"
        "/cancel - to cancel game\n"
        "/stat - to show stat\n"
        "/help - rules of the game and list of teams\n\n"
    )


@dp.message(Command("play"))
async def proceed_play(message: Message) -> None:
    if users[message.from_user.id]["in_game"] == True:
        await message.reply("You are in game. Send number instead.")
    else:
        fact = await get_random_fact()
        await message.reply(fact.event)
        users[message.from_user.id]["in_game"] = True
        users[message.from_user.id]["event_year"] = fact.year
        users[message.from_user.id]["total_games"] += 1


@dp.message(Command("cancel"))
async def proceed_cancel(message: Message) -> None:
    if users[message.from_user.id]["in_game"] == True:
        await message.reply("Current game cancelled")
        users[message.from_user.id]["attempts"] = 5
        users[message.from_user.id]["in_game"] = False
        users[message.from_user.id]["total_games"] -= 1
    else:
        await message.reply("Not in game - so no to cancel")


@dp.message(Command("stat"))
async def proceed_stat(message: Message) -> None:
    await message.reply(
        f"Statistic\n\n" f"Games: {users[message.from_user.id]['total_games']}\n" f"Wins: {users[message.from_user.id]['wins']}"
    )


@dp.message(lambda x: x.text and re.fullmatch(r"[-+]?\d*", x.text))
async def proceed_numbers(message: Message) -> None:
    if users[message.from_user.id]["in_game"] == False:
        await message.reply("You are not in game yet. Send /play to start.")
    else:
        if users[message.from_user.id]["attempts"] < 2:
            await message.reply(
                f"You lose! Answer is {users[message.from_user.id]['event_year']}."
            )
            users[message.from_user.id]["attempts"] = 5
            users[message.from_user.id]["in_game"] = False
            return
        usr_year = int(message.text)
        if usr_year == users[message.from_user.id]["event_year"]:
            await message.reply(f"That's right!")
            users[message.from_user.id]["attempts"] = 5
            users[message.from_user.id]["in_game"] = False
            users[message.from_user.id]["wins"] += 1
            return
        elif usr_year > users[message.from_user.id]["event_year"]:
            users[message.from_user.id]["attempts"] -= 1
            await message.reply(f"Too much. Attempts left: {users[message.from_user.id]['attempts']}")
        elif usr_year < users[message.from_user.id]["event_year"]:
            users[message.from_user.id]["attempts"] -= 1
            await message.reply(f"Too low. Attempts left: {users[message.from_user.id]['attempts']}")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
