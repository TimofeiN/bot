from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from app.messages import msg


# start menu keyboard
start_inline_kb = InlineKeyboardMarkup(row_width=1)
btn_weather = InlineKeyboardButton(text=msg.btn_weather_text, callback_data='weather_button')
btn_btc = InlineKeyboardButton(text=msg.btn_btc_menu, callback_data='btc_menu')
start_inline_kb.add(btn_weather, btn_btc)


# choose weather keyboard
cities_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

user_loc_btn = KeyboardButton(text=msg.loc_text, request_location=True)
tbi_btn = KeyboardButton(text=msg.btn_tbi_text)
bat_btn = KeyboardButton(text=msg.btn_bat_text)

cities_kb.row(tbi_btn, bat_btn)
cities_kb.add(user_loc_btn)


# bitcoin menu keyboard
btc_menu_kb = InlineKeyboardMarkup(row_width=1)



btn_show_price = InlineKeyboardButton(text=msg.btn_show_price_text, callback_data='btc_current_price')
btn_subscribe = InlineKeyboardButton(text=msg.btc_subscribe_text, callback_data='btc_add_subscription')
btn_show_subs = InlineKeyboardButton(text=msg.btc_show_subs_text, callback_data='btc_show_subscriptions')
btn_manage_subs = InlineKeyboardButton(text=msg.btc_manage_subs_text, callback_data='btc_manage_subscriptions')
btn_unsubscribe = InlineKeyboardButton(text=msg.btc_unsubscribe_text, callback_data='btc_unsubscribe_all')

btc_menu_kb.add(btn_show_price, btn_subscribe, btn_show_subs, btn_manage_subs, btn_unsubscribe)


# manage subscriptions keyboard
async def build_manage_kb(u_subscriptions, step=0):
    manage_subs_kb = InlineKeyboardMarkup(row_width=2)
    for sub in u_subscriptions:
        text = u_subscriptions[sub]
        data = sub
        manage_button = InlineKeyboardButton(text=text, callback_data=data)
        manage_subs_kb.add(manage_button)

    if step > 0:
        back_button = InlineKeyboardButton(text=msg.back, callback_data='back')
        confirm_button = InlineKeyboardButton(text=msg.confirm, callback_data='confirm')
        manage_subs_kb.row(back_button, confirm_button)
    return manage_subs_kb


# finish any btc action keyboard
btc_more_kb = InlineKeyboardMarkup(row_width=1)
btn_btc_more = InlineKeyboardButton(text="More actions with BTC", callback_data="btc_menu")
btc_more_kb.add(btn_btc_more)
