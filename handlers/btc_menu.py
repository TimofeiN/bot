import asyncio
import emoji

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_functions as db
import keyboards



async def btc_show_subscriptions(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    task_db = asyncio.create_task(db.db_main(db.show_subscriptions, user_id))
    res = await task_db
    u_subscriptions = ''
    for v in res:
        u_subscriptions += emoji.emojize(f':incoming_envelope: {res[v]}\n')
    answ_text = f'{user_name}, your subscriptions:\n' \
                f'{u_subscriptions}'
    await call.message.answer(text=answ_text)


async def unsubscribe_all(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    task_db = asyncio.create_task(db.db_main(db.unsubscribe_all, user_id))
    res = await task_db

    answ_text = f'{user_name}, {res}'
    await call.message.answer(text=answ_text)






# async def btc_subsc_start(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(text='Working on it')
#     await state.set_state(BtcFeedback.waiting_confirmation.state)
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add("Let's do it", "No thanx")
#     await call.message.answer('I can send you info about price drops', reply_markup=keyboard)

