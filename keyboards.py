from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import emoji



# start menu keyboard
start_inline_kb = InlineKeyboardMarkup(row_width=1)

btn_weather_text = f'Show weather {emoji.emojize(":thermometer:")}'
btn_btc_text = f'Show bitcoin price {emoji.emojize(":bar_chart:")}'

btn_weather = InlineKeyboardButton(text=btn_weather_text, callback_data='weather_button')
btn_btc = InlineKeyboardButton(text=btn_btc_text, callback_data='bitcoin_button')

start_inline_kb.add(btn_weather, btn_btc)


# choose weather keyboard
cities_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

emj_georgia = emoji.emojize(':Georgia:')
loc_text = f'MY LOCATION \N{world map}'

user_loc_btn = KeyboardButton(text=loc_text, request_location=True)
tbi_btn = KeyboardButton(text=f'TBILISI {emj_georgia}')
bat_btn = KeyboardButton(text=f'BATUMI {emj_georgia}')

cities_kb.row(tbi_btn, bat_btn)
cities_kb.add(user_loc_btn)


# bitcoin menu keyboard
btc_menu_kb = InlineKeyboardMarkup(row_width=1)

btc_subscribe_text = f'Add subscription'
btc_show_subs_text = f'Show current subscriptions'
btc_unsubscribe_text = f'Unsubscribe all'

btn_subscribe = InlineKeyboardButton(text=btc_subscribe_text, callback_data='btc_add_subscription')
btn_show_subs = InlineKeyboardButton(text=btc_show_subs_text, callback_data='btc_show_subscriptions')
btn_unsubscribe = InlineKeyboardButton(text=btc_unsubscribe_text, callback_data='btc_unsubscribe_all')

btc_menu_kb.add(btn_subscribe, btn_show_subs, btn_unsubscribe)
