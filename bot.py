import asyncio
import os
import logging
import sys
from os import getenv

import requests


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "8378017874:AAFJ307G9_oe9rmFr_qHGwxoTA9i49fD7hY" # i dont care about token btw

dp = Dispatcher()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def commandStartHandler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.first_name}! \nЭтот бот предназначен для удобного использования krch.io, отправь ссылку и получи сокращенную.")


@dp.message()
async def link_handler(message: Message) -> None:
    url = message.text
    if url is None:
        await message.answer("Пожалуйста, отправьте текстовое сообщение со ссылкой.")
        return
    
    if url.startswith("http://") or url.startswith("https://"):
        try:
            response = requests.post("https://localhost:443/api/links", json={"url": url})
            if response.status_code == 200:
                data = response.json()
                short_url = data.get("short_url")
                await message.answer(f"Сокращенная ссылка: {short_url}")
            else:
                await message.answer("Ошибка при сокращении ссылки. Попробуйте позже.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("Пожалуйста, отправьте действительную ссылку, начинающуюся с http:// или https://")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
