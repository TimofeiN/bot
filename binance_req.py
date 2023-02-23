import asyncio
from aiohttp import ClientSession
from decimal import Decimal


async def current(symbol):
    async with ClientSession() as session:
        url = f'https://api.binance.com/api/v3/ticker/24hr?type=MINI&symbol={symbol}'
        async with session.get(url) as response:
            reply = await response.json()

            last_price = Decimal(reply['lastPrice']).normalize()
            low_price = Decimal(reply['lowPrice']).normalize()
            high_price = Decimal(reply['highPrice']).normalize()
            return {'current_price': last_price,
                    'low_price': low_price,
                    'high_price': high_price}



            # return f"" \
            #        f"₿ current price - {current_price} $\n" \
            #        f"₿ min price 24h - {low_price} $\n" \
            #        f"₿ max price 24h - {high_price} $"

"""
async def main(symbol):
    task = asyncio.create_task(current(symbol))
    await task
    await asyncio.sleep(2)
    print(task.result())


while True:
    asyncio.run(main('BTCUSDT'))
"""
