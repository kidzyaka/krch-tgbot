import asyncio
import os
import logging
import sys
from os import getenv
from dotenv import load_dotenv
import json

import requests


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load.dotenv()

TOKEN =  os.getenv("TOKEN")


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
           
            payload = json.dumps(url)
            
            headers = {
                'Content-Type': 'Application/json'
            }

            print(url)

            response = requests.request("POST", "https://localhost:443/api/links", headers=headers, data=payload, verify=False)           
            if response.status_code == 201:
                try:
                    data = response.json()
                    shortURLcode = data.get("shortCode")
                    if shortURLcode:
                        await message.answer(f"Сокращенная ссылка: https://krch.io/{shortURLcode}")
                    else:
                        await message.answer("Ошибка: не удалось получить короткий код из ответа API.")
                except Exception as e:
                    await message.answer(f"Ошибка при обработке ответа API: {e}")
            else:
                await message.answer(f"Ошибка при сокращении ссылки. Код ответа: {response.status_code}")
        except Exception as e:
            await message.answer(f"Произошла ошибка при обращении к API: {e}")





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
