import asyncio
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

import app.weather_req as w_async
import app.keyboards as keyboards
from app.messages import msg


async def weather_start(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    await call.message.answer('Choose city', reply_markup=keyboards.cities_kb)


async def tbilisi_now(message: types.Message):
    w_task = asyncio.create_task(w_async.current_weather(*w_async.cities_dict['tbilisi']))
    msg_text = await w_task
    await message.reply(msg_text)


async def batumi_now(message: types.Message):
    w_task = asyncio.create_task(w_async.current_weather(*w_async.cities_dict['batumi']))
    msg_text = await w_task
    await message.reply(msg_text)


async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    w_task = asyncio.create_task(w_async.current_weather(lat, lon))
    msg_text = await w_task
    await message.reply(msg_text, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_weather(dp: Dispatcher):
    logging.info('register weather handlers')
    dp.register_callback_query_handler(weather_start, text='weather_button')
    dp.register_message_handler(tbilisi_now, Text(equals=msg.btn_tbi_text))
    dp.register_message_handler(batumi_now, lambda message: message.text == msg.btn_bat_text)
    dp.register_message_handler(handle_location, content_types=['location'])
