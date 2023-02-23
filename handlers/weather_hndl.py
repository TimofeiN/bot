import emoji
from aiogram import types
from aiogram.dispatcher.filters import Text
import weather_req as w_async


# @dp.message_handler(Text(equals=f'TBILISI {emoji.emojize(":Georgia:")}'))
async def tbilisi_now(message: types.Message):
    msg_text = await w_async.current_weather(*w_async.cities_dict['tbilisi'])
    await message.reply(msg_text)


# @dp.message_handler(lambda message: message.text == f'BATUMI {emoji.emojize(":Georgia:")}')
async def batumi_now(message: types.Message):
    msg_text = await w_async.main(*w_async.cities_dict['batumi'])
    await message.reply(msg_text)


# @dp.message_handler(content_types=['location'])
async def local_weather(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    msg_text = await w_async.main(lat, lon)
    await message.reply(msg_text, reply_markup=types.ReplyKeyboardRemove())


def register_weather_handlers(dp):
    dp.register_message_handler(tbilisi_now, Text(equals=f'TBILISI {emoji.emojize(":Georgia:")}'))
    dp.register_message_handler(batumi_now, Text(equals= f'BATUMI {emoji.emojize(":Georgia:")}'))
    dp.register_message_handler(local_weather, content_types=['location'])