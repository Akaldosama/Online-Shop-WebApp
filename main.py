import asyncio

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from telegram import WebAppInfo

API_TOKEN = '7525079654:AAFLaYwTC2niT3r7w3wDmFwvVc4kemWb7D0'


api = 'http://127.0.0.1:8000'
API_URL_REGISTER = f'{api}/registration/'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    start = State()
    contact = State()
    location = State()

user_data = {}

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     share_contact_button = types.KeyboardButton('Share Contact', request_contact=True)
#     send_location_button = types.KeyboardButton('Share Current Location', request_location=True)
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(share_contact_button, send_location_button)
#
#     await message.answer('Welcome! Would you like to share your contact or current location?', reply_markup=markup)
#     await Form.start.set()

def order_func():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Order Food', web_app=WebAppInfo(url='https://chic-crostata-4ad921.netlify.app/')))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    telegram_id = str(message.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json={"telegram_id": telegram_id}) as response:
            if response.status == 200:
                data = await response.json()
                name = data.get("name", "Пользователь")
                await message.answer(
                    f"Let's get started {name}🍟 \nPlease tap the button below to order your perfect lunch! 😃")
            else:
                await message.answer('Hello 👋. Welcome to @akaldobot 🤖.\nWith this bot you can order fast-food 🍔 🍕 🌭\n and we will deliver 🚚 it to you')
                await asyncio.sleep(2)
                await message.answer('For registration 🧾 please 🙏! Enter your name:')
                user_data[message.from_user.id] = {"telegram_id": telegram_id}

@dp.message_handler(lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
async def get_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text

    share_contact_button = types.KeyboardButton('Share Contact', request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(share_contact_button)

    await message.answer("Share your phone number:", reply_markup=markup)


@dp.message_handler(lambda message: message.from_user.id in user_data and 'phone' not in user_data[message.from_user.id])
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone'] = message.text
    await message.answer("Let's get started 🍟\n Please tap the button below to order your perfect lunch!", reply_markup=)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)