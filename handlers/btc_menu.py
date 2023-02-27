import asyncio
import emoji

from aiogram import Dispatcher, types
import db_functions as db


async def btc_show_subscriptions(call: types.CallbackQuery):
    await call.answer(text='ერთი წამი')
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    task_db = asyncio.create_task(db.db_main(db.show_subscriptions, user_id))
    res = await task_db

    answ_text = f'{user_name}, {res}'
    await call.message.answer(text=answ_text)


async def unsubscribe_all(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    task_db = asyncio.create_task(db.db_main(db.unsubscribe_all, user_id))
    res = await task_db

    answ_text = f'{user_name}, {res}'
    await call.message.answer(text=answ_text)
