import asyncio
import decimal

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db_functions import main


class BtcFeedback(StatesGroup):
    waiting_confirmation = State()
    waiting_price_method = State()
    waiting_price_value = State()


async def btc_subsc_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='ერთი წამი')
    await state.set_state(BtcFeedback.waiting_confirmation.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Let's do it", "No thanx")
    await call.message.answer('I can send you info about price drops', reply_markup=keyboard)


async def btc_subsc_price_type(message: types.Message, state: FSMContext):
    if not message.text.lower() == "let's do it":
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
        await message.answer('You need to choose price param')
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
        price = 1 - decimal.Decimal(msg_txt[:-1]) / 100
    else:
        if not (msg_txt[-2:-1].isdigit() and msg_txt[1:-3].isdigit()):
            await message.answer('Please type your price in correct format. Example 12345.78')
            return
    await state.update_data(price_val=msg_txt)

    user_params = await state.get_data()
    u_name = user_params['u_name']
    u_id = user_params['u_id']
    print(user_params)
    task_db = asyncio.create_task(main(user_params))
    await task_db
    answ_text = emoji.emojize(
        f"Hi, {u_name} :waving_hand: \n"
        f"Your :ID_button: is: {u_id}\n"
        f"price in percent: {user_params['price_type_percent']} \nprice value {user_params['price_val']}\n"
        f"{task_db.result()}")
    await message.answer(text=answ_text)
    await state.reset_state(with_data=False)


def register_handlers_btc_subscr(dp: Dispatcher):
    print('register handlers')
    dp.register_callback_query_handler(btc_subsc_start, text="btc_more", state="*")
    dp.register_message_handler(btc_subsc_price_type, state=BtcFeedback.waiting_confirmation)
    dp.register_message_handler(bts_subscr_price_value, state=BtcFeedback.waiting_price_method)
    dp.register_message_handler(bts_subscr_u_params, state=BtcFeedback.waiting_price_value)
