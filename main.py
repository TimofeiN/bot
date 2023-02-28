import asyncio

import emoji
import logging
# import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from handlers.btc_subscription import register_handlers_btc_subscr
from back.xconfig import GHV_TOKEN
import binance_req as bin_async
import weather_req as w_async
import keyboards as kb
from message_sender import message_sender
import handlers.btc_menu
from messages import msg


# import pip
# from background import keep_alive
# pip.main(['install', 'aiogram'])


logging.basicConfig(level=logging.INFO)
TOKEN = GHV_TOKEN
storage = RedisStorage2(db=1)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    # text = emoji.emojize('Hi! :victory_hand:'
    #                      'Write me smth. or press /help')
    await message.reply(msg.welcome)


@dp.message_handler(commands=['cancel'], state="*")
@dp.message_handler(Text(equals="No thanx", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='weather_button')
async def send_weather(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    await call.message.answer('Choose city', reply_markup=kb.cities_kb)


@dp.callback_query_handler(text='bitcoin_button')
async def send_btc_info(call: types.CallbackQuery):
    await call.answer(text='ერთი წამი')
    btc_task = asyncio.create_task(bin_async.current('BTCUSDT'))
    btc_now = await btc_task
    msg_text = f"" \
               f"₿ current price - {btc_now['current_price']} $usdt\n" \
               f"₿ min price 24h - {btc_now['low_price']} $usdt\n" \
               f"₿ max price 24h - {btc_now['high_price']} $usdt"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="More actions with BTC", callback_data="btc_more"))
    await call.message.answer(msg_text, reply_markup=keyboard)


# btc_menu_handler -> 'btc_more'
@dp.callback_query_handler(text='btc_more')
async def btc_menu(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    await call.message.answer('Choose option', reply_markup=kb.btc_menu_kb)


@dp.message_handler(Text(equals=f'TBILISI {emoji.emojize(":Georgia:")}'))
async def tbilisi_now(message: types.Message):
    w_task = asyncio.create_task(w_async.current_weather(*w_async.cities_dict['tbilisi']))
    msg_text = await w_task
    await message.reply(msg_text)


@dp.message_handler(lambda message: message.text == f'BATUMI {emoji.emojize(":Georgia:")}')
async def batumi_now(message: types.Message):
    w_task = asyncio.create_task(w_async.current_weather(*w_async.cities_dict['batumi']))
    msg_text = await w_task
    await message.reply(msg_text)


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    w_task = asyncio.create_task(w_async.current_weather(lat, lon))
    msg_text = await w_task
    await message.reply(msg_text, reply_markup=types.ReplyKeyboardRemove())


register_handlers_btc_subscr(dp)
dp.register_callback_query_handler(handlers.btc_menu.btc_show_subscriptions, text='btc_show_subscriptions')
dp.register_callback_query_handler(handlers.btc_menu.unsubscribe_all, text='btc_unsubscribe_all')

handlers.btc_menu.register_handler_manage_subs(dp)
# weather_hndl.register_weather_handlers(dp)


@dp.message_handler()
@dp.message_handler(commands=['help'])
async def echo(message: types.Message):
    await message.answer(message.text)
    await message.answer('What can I do:', reply_markup=kb.start_inline_kb)


async def on_shutdown(dp: Dispatcher):
    # Close Redis connection
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Storage Connection closed")


async def start_binance(sleep_time):
    while True:
        await asyncio.sleep(sleep_time)
        await message_sender()


async def on_startup(dp: Dispatcher):
    asyncio.create_task(start_binance(10))


if __name__ == '__main__':
    # keep_alive()
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)
