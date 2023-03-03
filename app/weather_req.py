# import asyncio
from aiohttp import ClientSession
from back.xconfig import OW_TOKEN
from app.messages import msg


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


async def current_weather(lat, lon):
    async with ClientSession() as session:
        weather_now = f'https://api.openweathermap.org/data/2.5/weather?' \
                      f'lat={lat}&lon={lon}&units=metric&appid={OW_TOKEN}'
        async with session.get(weather_now) as response:
            reply = await response.json()

            city_name = reply['name']
            description = reply['weather'][0]['description']
            temp = reply['main']['temp']
            f_l_temp = reply['main']['feels_like']
            wind_speed = reply['wind']['speed']
            wind_degr = reply['wind']['deg']
            wind_dir = wind_converter(wind_degr)

            return msg.weather_answer.format(city_name=city_name, description=description, temp=temp, f_l_temp=f_l_temp,
                                             wind_speed=wind_speed, wind_degr=wind_degr, wind_dir=wind_dir)


cities_dict = {
    'tbilisi': ['41.77', '44.81'],
    'batumi': ['41.65', '41.63']
}

"""
async def main(lat, lon):
    task = asyncio.create_task(current_weather(lat, lon))
    await task
    print('..')
    await asyncio.sleep(2)
    print(task.result())


while True:
    asyncio.run(main(*cities_dict['batumi']))
"""
