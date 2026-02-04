import asyncio
import os
import logging
import sys
from os import getenv


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "8378017874:AAFJ307G9_oe9rmFr_qHGwxoTA9i49fD7hY"

dp = Dispatcher()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def commandStartHandler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.first_name}! \nЭтот бот предназначен для удобного использования krch.io, отправь ссылку и получи сокращенную.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())









