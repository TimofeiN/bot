import asyncio
import datetime
import json
from requests import get
from back.xconfig import OW_TOKEN


def tbi_weather():
    ow_tok = OW_TOKEN
    tbi = f'https://api.openweathermap.org/data/2.5/forecast?lat=41.77&cnt=10&units=metric&lon=44.81&appid={ow_tok}'

    reply = json.loads(get(tbi).text)
    now = reply['list'][0]

    city = reply['city']['name']
    time = reply['list'][0]['dt_txt'][-8:]
    clouds = now['clouds']['all']
    temp = now['main']['temp']
    temp_fl = now['main']['feels_like']
    wind_speed = now['wind']['speed']
    prsip_percent = now['pop']

    result = f"""
        "{city}" {time} 
         облачность {clouds}%
         температура {temp} С
         ощущается {temp_fl} С
         ветер {wind_speed} m/s
         вероятность осадков {prsip_percent}%
    """
    return result


def wind_converter(wind_dir_deg):
    wind_rad = ''
    if 337 < wind_dir_deg <= 360 or 0 <= wind_dir_deg <= 22:
        wind_rad = 'N'
    elif 22 < wind_dir_deg <= 67:
        wind_rad = 'NE'
    elif 67 < wind_dir_deg <= 112:
        wind_rad = 'E'
    elif 112 < wind_dir_deg <= 157:
        wind_rad = 'SE'
    elif 157 < wind_dir_deg <= 202:
        wind_rad = 'S'
    elif 202 < wind_dir_deg <= 247:
        wind_rad = 'SW'
    elif 247 < wind_dir_deg <= 292:
        wind_rad = 'W'
    elif 293 < wind_dir_deg <= 337:
        wind_rad = 'NW'
    return wind_rad


def time_from_unix(dt):
    value = datetime.datetime.fromtimestamp(dt)
    hum_dt = value.strftime('%Y-%m-%d %H:%M:%S')
    return hum_dt[-8:]


def current_weather(lat, lon):
    ow_tok = OW_TOKEN

    weather_now = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={ow_tok}'
    reply = json.loads(get(weather_now).text)
    # pprint(reply)

    city_name = reply['name']
    description = reply['weather'][0]['description']
    temp = reply['main']['temp']
    f_l_temp = reply['main']['feels_like']
    wind_speed = reply['wind']['speed']
    wind_degr = reply['wind']['deg']
    wind_dir = wind_converter(wind_degr)

    return f'In {city_name} now: {description}\n' \
           f'{temp}°C feels like {f_l_temp}°C \n' \
           f'wind {wind_dir} speed {wind_speed} m/s'


cities_dict = {
    'tbilisi': ['41.77', '44.81'],
    'batumi': ['41.65', '41.63']
}


# print(current_weather(*cities_dict['tbilisi']))
