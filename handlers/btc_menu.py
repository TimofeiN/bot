import asyncio
import emoji

from aiogram import Dispatcher, types
import db_functions as db


async def btc_show_subscriptions(call: types.CallbackQuery):
    await call.answer(text='ერთი წამი')
    user_id = call.from_user.id
    task_db = asyncio.create_task(db.db_main(db.show_subscriptions, user_id))
    await task_db

    answ_text = f'{task_db.result()}'
    await call.message.answer(text=answ_text)
