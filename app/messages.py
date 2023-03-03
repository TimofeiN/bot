from dataclasses import dataclass
from emoji import emojize


@dataclass(frozen=True)
class Messages:
    welcome: str = emojize('Hi! :victory_hand: \n'
                           'Write me smth. or press /help')

    btn_weather_text: str = f'Show weather {emojize(":thermometer:")}'
    btn_btc_menu: str = f'Bitcoin options'

    btn_show_price_text: str = f'Show bitcoin price {emojize(":bar_chart:")}'

    emj_georgia: str = emojize(':Georgia:')
    loc_text: str = f'MY LOCATION \N{world map}'
    btn_tbi_text: str = f'TBILISI {emj_georgia}'
    btn_bat_text: str = f'BATUMI {emj_georgia}'

    back: str = emojize(':right_arrow_curving_left: back')
    confirm: str = emojize(':check_mark_button: confirm')

    weather_answer: str = "In {city_name} now: {description}\n" \
                          "{temp}°C, feels like {f_l_temp}°C \n" \
                          "wind {wind_dir} speed {wind_speed} m/s"


msg = Messages()
