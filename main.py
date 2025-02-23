# import asyncio
# import aiohttp
# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils import executor
# from telegram import WebAppInfo
#
# API_TOKEN = '7525079654:AAFLaYwTC2niT3r7w3wDmFwvVc4kemWb7D0'
#
#
# api = 'http://127.0.0.1:8000'
# API_URL_REGISTER = f'{api}/users/'
#
# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
#
# user_data = {}
# # @dp.message_handler(commands=['start'])
# # async def start(message: types.Message):
# #     share_contact_button = types.KeyboardButton('Share Contact', request_contact=True)
# #     send_location_button = types.KeyboardButton('Share Current Location', request_location=True)
# #
# #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(share_contact_button, send_location_button)
# #
# #     await message.answer('Welcome! Would you like to share your contact or current location?', reply_markup=markup)
# #     await Form.start.set()
#
#
# def order_func():
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Order Food', web_app=WebAppInfo(url='https://online-shop-webapp.netlify.app/')))
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     telegram_id = str(message.from_user.id)
#     async with aiohttp.ClientSession() as session:
#         async with session.post(API_URL_REGISTER, json={"telegram_id": telegram_id}) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 name = data.get("name", "Пользователь")
#                 await message.answer(
#                     f"Let's get started {name}🍟 \nPlease tap the button below to order your perfect lunch! 😃", reply_markup=order_func())
#             else:
#                 await message.answer('Hello 👋. Welcome to @akaldodeliverybot 🤖.\nWith this bot you can order fast-food 🍔 🍕 🌭\n and we will deliver 🚚 it to you')
#                 await asyncio.sleep(2)
#                 await message.answer('For registration 🧾 please 🙏! Enter your name:')
#                 user_data[message.from_user.id] = {}
#
# @dp.message_handler(lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
# async def get_name(message: types.Message):
#     user_data[message.from_user.id]['name'] = message.text
#
#     share_contact_button = types.KeyboardButton('Share Contact', request_contact=True)
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(share_contact_button)
#
#     await message.answer("Share your phone number:", reply_markup=markup)
#
#
# @dp.message_handler(lambda message: message.from_user.id in user_data and 'phone' not in user_data[message.from_user.id])
# async def get_phone(message: types.Message):
#     telegram_id = message.from_user.id
#     user_data[telegram_id]['phone'] = message.text
#     payload = {
#         "telegram_id": telegram_id,
#         "name": user_data[telegram_id]['name'],
#         "phone": user_data[telegram_id]['phone']
#     }
#
#     async with aiohttp.ClientSession() as session:
#         async with session.post(API_URL_REGISTER, json=payload) as response:
#             if response.status == 200:
#                 await message.answer("You are registered successfully!🎉✨")
#                 await asyncio.sleep(2)
#                 await message.answer("Let's get started 🍟\nPlease tap the button below to order 🛒 your perfect lunch! 😋🍴", reply_markup=order_func())
#             else:
#                 error_message = (await response.json()).get('error', 'Xato yuz berdi.')
#                 await message.answer(f"Xatolik: {error_message}")
#
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)


import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
# from telegram import WebAppInfo
from aiogram.types.web_app_info import WebAppInfo


API_TOKEN = '7525079654:AAFLaYwTC2niT3r7w3wDmFwvVc4kemWb7D0'
API_URL = 'https://online-shop-webapp.netlify.app'
API_URL_REGISTER = f'{API_URL}/api/users/'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}


def order_func():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            'Order Food', web_app=WebAppInfo(url='https://online-shop-webapp.netlify.app/items/')
        )
    )
    return markup  # RETURN the markup


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    telegram_id = str(message.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json={"telegram_id": telegram_id}) as response:
            if response.status == 200:
                data = await response.json()
                name = data.get("name", "Пользователь")
                await message.answer(
                    f"Let's get started {name}🍟 \nPlease tap the button below to order your perfect lunch! 😃",
                    reply_markup=order_func()  # USE THE FUNCTION RETURN VALUE
                )
            else:
                await message.answer('Hello 👋. Welcome to @akaldodeliverybot 🤖.\nWith this bot you can order fast-food 🍔 🍕 🌭\n and we will deliver 🚚 it to you')
                await asyncio.sleep(1)
                await message.answer('For registration 🧾 please 🙏! Enter your name:')
                user_data[message.from_user.id] = {}



@dp.message_handler(lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
async def get_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton('Share Contact', request_contact=True)
    )
    await message.answer("Please share your phone number:", reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message):
    telegram_id = message.from_user.id
    user_data[telegram_id]['phone'] = message.contact.phone_number
    payload = {
        "telegram_id": telegram_id,
        "name": user_data[telegram_id]['name'],
        "phone": user_data[telegram_id]['phone']
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json=payload) as response:
            if response.status == 201:
                await message.answer("Registration successful! 🎉✨")
                await asyncio.sleep(2)
                await message.answer("Now you can order food! Tap the button below. 🍟", reply_markup=order_button())
            else:
                await message.answer("An error occurred during registration. Please try again.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
