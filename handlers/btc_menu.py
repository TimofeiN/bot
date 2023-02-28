import asyncio
import emoji

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_functions as db
import keyboards
from main import bot


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


class ManageSubscriptions(StatesGroup):
    sub_start_manage = State()
    sub_waiting_unsubscribe = State()


async def manage_subscriptions_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Working on it')
    await state.set_state(ManageSubscriptions.sub_start_manage.state)

    u_id = call.from_user.id
    db_task = asyncio.create_task(db.db_main(db.show_subscriptions, u_id))
    u_subscriptions = await db_task
    kb_task = asyncio.create_task(keyboards.build_manage_kb(u_subscriptions))
    kb = await kb_task

    await state.update_data(u_subscriptions)
    await call.message.reply(text='press to unsubscribe', reply_markup=kb)
    # print(r_data)      #  {'79': 'price value 10.00%', '80': 'price value 23900.99$', '81': 'price value 5.00%'}





async def manage_subscriptions_choice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Working on it')
    u_subscriptions = await state.get_data()
    data = call.data
    symbol = emoji.emojize(':prohibited:')
    u_subscriptions[data] = f'{symbol} {u_subscriptions[data]}'

    kb_task = asyncio.create_task(keyboards.build_manage_kb(u_subscriptions, step=1))
    kb = await kb_task

    await bot.edit_message_reply_markup(reply_markup=kb)

    print(u_subscriptions)
    print(u_subscriptions[data])


async def manage_subscriptions_any_msg(message: types.Message):
    await message.reply('Use buttons or press /cancel')


def register_handler_manage_subs(dp: Dispatcher):
    dp.register_callback_query_handler(manage_subscriptions_start, text='btc_manage_subscriptions', state="*")
    dp.register_callback_query_handler(manage_subscriptions_choice, state=ManageSubscriptions.sub_start_manage.state)
    dp.register_message_handler(manage_subscriptions_any_msg, state=ManageSubscriptions.sub_start_manage.state)




# async def btc_subsc_start(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(text='Working on it')
#     await state.set_state(BtcFeedback.waiting_confirmation.state)
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add("Let's do it", "No thanx")
#     await call.message.answer('I can send you info about price drops', reply_markup=keyboard)

