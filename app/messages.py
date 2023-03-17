from dataclasses import dataclass
from emoji import emojize


# Most of the text variables used in the project
@dataclass(frozen=True)
class Messages:
    welcome: str = emojize('Hi! :victory_hand: \n'
                           'Write me smth. or press /help')

    btn_weather_text: str = f'Show weather {emojize(":thermometer:")}'
    btn_btc_menu: str = f'Bitcoin options {emojize(":coin:")}'

    btn_show_price_text: str = f'Show bitcoin price {emojize(":bar_chart:")}'
    btc_subscribe_text = f'Add subscription {emojize(":envelope_with_arrow:")}'
    btc_show_subs_text = f'Show current subscriptions {emojize(":incoming_envelope:")} '
    btc_manage_subs_text = f'Manage current subscriptions {emojize(":counterclockwise_arrows_button:")}'
    btc_unsubscribe_text = f'Unsubscribe all {emojize(":no_entry:")}'

    emj_georgia: str = emojize(':Georgia:')
    loc_text: str = f'MY LOCATION \N{world map}'
    btn_tbi_text: str = f'TBILISI {emj_georgia}'
    btn_bat_text: str = f'BATUMI {emj_georgia}'

    back: str = emojize(':right_arrow_curving_left: back')
    confirm: str = emojize(':check_mark_button: confirm')

    weather_answer: str = "In {city_name} now: {description}\n" \
                          "{temp}°C, feels like {f_l_temp}°C \n" \
                          "wind {wind_dir} speed {wind_speed} m/s"

    price_drop: str = emojize("It's time to buy. :chart_decreasing:\n"
                              "Now price is {current_price}\n" 
                              "Your :money_bag: profit:\n"
                              "{profit} $ from one ₿")


msg = Messages()
