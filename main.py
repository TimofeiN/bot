import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from back.xconfig import GHV_TOKEN
from app.handlers.btc_subscription import register_handlers_btc_subscr
from app.handlers.weather_hndl import register_handlers_weather

import app.keyboards as keyboards
import app.handlers.btc_menu as bitcoin_menu

from message_sender import message_sender
from app.messages import msg

# import for public hosting
# import pip
# from back.background import keep_alive


logging.basicConfig(level=logging.INFO)
TOKEN = GHV_TOKEN
storage = RedisStorage2(db=1)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.reply(msg.welcome)


@dp.message_handler(commands=['cancel'], state="*")
@dp.message_handler(Text(equals="No thanx", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


register_handlers_btc_subscr(dp)
register_handlers_weather(dp)
bitcoin_menu.register_handlers_manage_subs(dp)
dp.register_callback_query_handler(bitcoin_menu.btc_menu, text='btc_menu')
dp.register_callback_query_handler(bitcoin_menu.btc_show_current, text='btc_current_price')
dp.register_callback_query_handler(bitcoin_menu.btc_show_subscriptions, text='btc_show_subscriptions')
dp.register_callback_query_handler(bitcoin_menu.unsubscribe_all, text='btc_unsubscribe_all')


@dp.message_handler()
@dp.message_handler(commands=['help'])
async def echo(message: types.Message):

    await message.answer(message.text)
    await message.reply('What can I do:', reply_markup=keyboards.start_inline_kb)


# main functions
async def on_shutdown(dp: Dispatcher):
    # Close Redis connection
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Storage Connection closed")


# Run message sender in background
async def on_startup(dp: Dispatcher):
    asyncio.create_task(message_sender())


if __name__ == '__main__':
    # keep_alive()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
