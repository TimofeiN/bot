import asyncpg
import asyncio
import logging
from back.xconfig import db_user, db_passwd
from binance_req import current

"""
to use:
async def iterate(con: Connection):
    async with con.transaction():
        async for record in stmt.cursor(10):
            print(record)
"""


async def iterate():
    con = await asyncpg.connect(host='localhost', database='test', user=db_user, password=db_passwd)
    async with con.transaction():
        async for record in con.cursor(f'''
                    SELECT u."name", u.btc_subscription, us.user_id, us.price_type_percent, us.price_value FROM users u 
                    JOIN users_subscriptions us ON us.user_id=u.user_id
                    WHERE btc_subscription IS TRUE;'''):
            task1 = asyncio.create_task(current("BTCUSDT"))
            cur_price = await task1
            user_id = record['user_id']
            percent = record['price_type_percent']

            if percent:
                user_price = record['price_value'] * cur_price['high_price']
            else:
                user_price = record['price_value']

            if cur_price['current_price'] <= user_price:
                # logging.info(f'   --> sending msg to user_id #{user_id}')
                print(f'   --> sending msg to user_id #{user_id}')


async def message_sender():
    task = asyncio.create_task(iterate())
    await task
    # print('sleep')
    await asyncio.sleep(5)


"""
while True:
    asyncio.run(message_sender())
"""
