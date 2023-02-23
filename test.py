import asyncpg
import asyncio
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
                    SELECT u.user_id, u.price_value, u.price_type_percent 
                    FROM users_subscriptions u'''):
            task1 = asyncio.create_task(current("BTCUSDT"))
            cur_price = await task1
            user_id = record['user_id']
            percent = record['price_type_percent']

            if percent:
                user_price = record['price_value'] * cur_price['high_price']
            else:
                user_price = record['price_value']
            print(f'id {user_id} - price{user_price} | current{cur_price["current_price"]} | '
                  f'max{cur_price["high_price"]}')

            if cur_price['current_price'] <= user_price:
                print(f'   --> sending msg to user_id #{user_id}')


async def message_sender():
    task = asyncio.create_task(iterate())
    await task
    print('sleep')
    await asyncio.sleep(5)


for i in range(3):
    asyncio.run(message_sender())
