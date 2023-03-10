import asyncio
import logging
import emoji

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_functions as db
import app.keyboards as keyboards


class BtcFeedback(StatesGroup):
    waiting_confirmation = State()
    waiting_price_method = State()
    waiting_price_value = State()


async def btc_subsc_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Working on it')
    await state.set_state(BtcFeedback.waiting_confirmation.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Let's do it", "No thanx")
    await call.message.answer('I can send you info about price drops', reply_markup=keyboard)


async def btc_subsc_price_type(message: types.Message, state: FSMContext):
    if not message.text.lower() == "let's do it":
        await message.answer('Use buttons or press /cancel')
        return
    await state.update_data(u_id=message.from_user.id)
    await state.update_data(u_name=message.from_user.first_name)
    await state.set_state(BtcFeedback.waiting_price_method.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('in percent %', 'Absolutely price')
    await message.answer(
        'Want to set your absolutely price or percent of the maximum 24 hours price', reply_markup=keyboard)


async def bts_subscr_price_value(message: types.Message, state: FSMContext):
    if not (message.text.lower() == "in percent %" or message.text.lower() == "absolutely price"):
        await message.answer('Use buttons or press /cancel')
        return
    await state.set_state(BtcFeedback.waiting_price_value.state)

    if message.text.lower() == "in percent %":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
        await state.update_data(price_type_percent=True)
        keyboard.add("2%", "5%", "10%")
        await message.answer('Choose one option', reply_markup=keyboard)

    elif message.text.lower() == "absolutely price":
        await state.update_data(price_type_percent=False)
        await message.answer('Type your price in numbers with 2 decimal digits. '
                             'For example 22500.99')


async def bts_subscr_u_params(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    price_type = state_data['price_type_percent']
    msg_txt = message.text

    if price_type is True:
        if msg_txt not in ["2%", "5%", "10%"]:
            await message.answer('You need to choose one option.Use special keyboard buttons')
            return
    else:
        if not (msg_txt[-2:-1].isdigit() and msg_txt[1:-3].isdigit()):
            await message.answer('Please type your price in correct format. Example 12345.78')
            return
    await state.update_data(price_val=msg_txt)

    user_params = await state.get_data()
    print(user_params)
    task_db = asyncio.create_task(db.db_main(db.add_user_subscription, user_params))
    db_res = await task_db

    u_name = user_params['u_name']
    percent = user_params['price_type_percent']
    u_price = user_params['price_val']
    if percent:
        symbol = ''
    else:
        symbol = '$'
    answ_text = emoji.emojize(
        f"Hi, {u_name} :waving_hand: \n"
        f"{db_res}:\n"
        f":incoming_envelope: price value {u_price}{symbol}\n"
        )

    await message.answer(text=answ_text, reply_markup=keyboards.btc_more_kb)
    await state.reset_state()


def register_handlers_btc_subscr(dp: Dispatcher):
    logging.info('register btc_subscription handlers')
    dp.register_callback_query_handler(btc_subsc_start, text="btc_add_subscription", state="*")
    dp.register_message_handler(btc_subsc_price_type, state=BtcFeedback.waiting_confirmation)
    dp.register_message_handler(bts_subscr_price_value, state=BtcFeedback.waiting_price_method)
    dp.register_message_handler(bts_subscr_u_params, state=BtcFeedback.waiting_price_value)
