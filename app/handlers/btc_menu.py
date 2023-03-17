"""
Script for Bitcoin menu except adding new subscription
"""
import asyncio
import logging

import emoji
from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import db_functions as db
import app.binance_req as bin_async
import app.keyboards as keyboards


async def btc_menu(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    bot = Bot.get_current()
    msg_id = call.message.message_id
    chat_id = call.from_user.id
    await bot.edit_message_reply_markup(message_id=msg_id, chat_id=chat_id, reply_markup=None)
    await call.message.answer('Choose option', reply_markup=keyboards.btc_menu_kb)


async def btc_show_current(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    btc_task = asyncio.create_task(bin_async.current('BTCUSDT'))
    btc_now = await btc_task
    msg_text = f"" \
               f"₿ current price - {round(btc_now['current_price'], 2)} $usdt\n" \
               f"₿ min price 24h - {round(btc_now['low_price'], 2)} $usdt\n" \
               f"₿ max price 24h - {round(btc_now['high_price'], 2)} $usdt"
    await call.message.answer(msg_text, reply_markup=keyboards.btc_more_kb)


async def btc_show_subscriptions(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    task_db = asyncio.create_task(db.db_main(db.show_subscriptions, user_id))
    res = await task_db
    answer_txt = f'{user_name}, '
    if res:
        u_subscriptions = f'your subscriptions:\n'
        for v in res:
            u_subscriptions += emoji.emojize(f':envelope: {res[v]}\n')
        answer_txt += f'{u_subscriptions}'
    else:
        answer_txt += f'no subscriptions added'

    await call.message.answer(text=answer_txt, reply_markup=keyboards.btc_more_kb)


async def unsubscribe_all(call: types.CallbackQuery):
    await call.answer(text='Working on it')
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    task_db = asyncio.create_task(db.db_main(db.unsubscribe_all, user_id))
    res = await task_db
    answ_text = f'{user_name}, {res}'
    await call.message.answer(text=answ_text, reply_markup=keyboards.btc_more_kb)


# Manage user's subscriptions functions using Redis FSM
class ManageSubscriptions(StatesGroup):
    start_manage = State()


async def manage_subscriptions_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Working on it')
    u_id = call.from_user.id
    db_task = asyncio.create_task(db.db_main(db.show_subscriptions, u_id))
    u_subscriptions = await db_task

    if not u_subscriptions:
        await call.message.answer(text='No subscriptions added')
        return

    await state.set_state(ManageSubscriptions.start_manage.state)
    kb_task = asyncio.create_task(keyboards.build_manage_kb(u_subscriptions))
    kb = await kb_task
    await state.update_data(u_subscriptions)
    await call.message.answer(text='press to unsubscribe', reply_markup=kb)


async def manage_subscriptions_choice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Choose subscriptions to delete')
    msg_id = call.message['message_id']
    chat_id = call.message["chat"]["id"]
    bot = Bot.get_current()
    u_subscriptions = await state.get_data()
    call_data = call.data
    symbol = emoji.emojize(':prohibited:')

    if call_data.isdigit():
        if u_subscriptions[call_data].startswith(symbol):
            return

        await state.update_data({call_data: f'{symbol} {u_subscriptions[call_data]}'})
        new_state_data = await state.get_data()

        kb_task = asyncio.create_task(keyboards.build_manage_kb(new_state_data, step=1))
        kb = await kb_task

        await bot.edit_message_reply_markup(message_id=msg_id, chat_id=chat_id, reply_markup=kb)
        return

    elif call_data == 'back':
        await state.reset_state()
        await bot.delete_message(message_id=msg_id, chat_id=chat_id)
        return

    unsub_lst = []
    for k in u_subscriptions:
        if u_subscriptions[k].startswith(symbol):
            unsub_lst.append(int(k))
    logging.info(f'{unsub_lst} - subscriptions deleted:')
    db_task = asyncio.create_task(db.db_main(db.remove_subscription, unsub_lst))
    res = await db_task
    await state.reset_state()
    await bot.delete_message(message_id=msg_id, chat_id=chat_id)
    await call.message.answer(text=res, reply_markup=keyboards.btc_more_kb)


async def manage_subscriptions_any_msg(message: types.Message):
    await message.reply('Use buttons or press /cancel')


def register_handlers_manage_subs(dp: Dispatcher):
    logging.info('register manage handlers')
    dp.register_callback_query_handler(manage_subscriptions_start, text='btc_manage_subscriptions', state='*')
    dp.register_callback_query_handler(manage_subscriptions_choice, state=ManageSubscriptions.start_manage)
    dp.register_message_handler(manage_subscriptions_any_msg, state=ManageSubscriptions.states)
