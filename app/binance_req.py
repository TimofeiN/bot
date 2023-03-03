# import asyncio
from aiohttp import ClientSession
from decimal import Decimal


async def current(symbol):
    async with ClientSession() as session:
        url = f'https://api.binance.com/api/v3/ticker/24hr?type=MINI&symbol={symbol}'
        async with session.get(url) as response:
            reply = await response.json()

            last_price = Decimal(reply['lastPrice'])
            low_price = Decimal(reply['lowPrice'])
            high_price = Decimal(reply['highPrice'])
            return {'current_price': last_price,
                    'low_price': low_price,
                    'high_price': high_price}


"""
async def main(symbol):
    task = asyncio.create_task(current(symbol))
    await task
    await asyncio.sleep(2)
    print(task.result())


while True:
    asyncio.run(main('BTCUSDT'))
"""
