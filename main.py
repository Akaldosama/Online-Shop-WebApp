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
API_URL = 'https://71e7-213-206-61-98.ngrok-free.app'
API_URL_REGISTER = f'{API_URL}/api/users/'
API_URL_ORDER = "http://127.0.0.1:8000/api/orders/create-order/"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}


def order_func():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            'Order Food', web_app=WebAppInfo(url='https://71e7-213-206-61-98.ngrok-free.app/items/')
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
    """Handles user registration after receiving phone contact"""
    telegram_id = message.from_user.id

    if telegram_id not in user_data:
        await message.answer("❌ Something went wrong. Please restart with /start.")
        return

    user_data[telegram_id]['phone'] = message.contact.phone_number

    # Prepare request payload
    payload = {
        "telegram_id": telegram_id,
        "name": user_data[telegram_id]['name'],
        "phone": user_data[telegram_id]['phone']
    }

    # Send registration request to backend API
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json=payload) as response:
            if response.status == 201:
                await message.answer("✅ Registration successful! 🎉✨")
                await asyncio.sleep(1)
                await message.answer("Now you can order food! 🍔", reply_markup=order_func())
            else:
                await message.answer("❌ Registration failed. Please try again using /start.")

    # Remove user data from temporary storage
    user_data.pop(telegram_id, None)


@dp.message_handler(commands=['order'])
async def order_food(message: types.Message):
    """Handles food ordering and asks for location"""
    telegram_id = message.from_user.id

    if telegram_id not in user_data:
        await message.answer("⚠️ Please register first using /start.")
        return

    # Dummy example: assuming the user selects items
    user_data[telegram_id]['order'] = [
        {"id": 1, "name": "Burger", "price": 5, "quantity": 2},
        {"id": 2, "name": "Pizza", "price": 10, "quantity": 1}
    ]

    payload = {
        "user_id": telegram_id,
        "items": [item["id"] for item in user_data[telegram_id]['order']]
    }

    # Send order request to backend API
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_ORDER, json=payload) as response:
            if response.status == 201:
                await message.answer("✅ Your order has been placed! Now, please share your location for delivery. 📍")

                # 📌 ASK FOR LOCATION
                location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                location_keyboard.add(KeyboardButton("📍 Share Location", request_location=True))

                await message.answer("📍 Tap the button below to send your location.", reply_markup=location_keyboard)
            else:
                await message.answer("⚠️ Order failed. Please try again later.")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message):
    """Handles user location after placing an order"""
    telegram_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    user_location = {
        "telegram_id": telegram_id,
        "latitude": latitude,
        "longitude": longitude
    }

    # Send location data to backend API
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_ORDER, json=user_location) as response:
            if response.status == 200:
                await message.answer("🚀 Thank you! Your order is on the way. 🍽️")
            else:
                await message.answer("⚠️ Something went wrong. Please try again.")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
