import asyncio
import asyncpg
import decimal
from pprint import pprint
from back.xconfig import db_user, db_passwd

# redis_data = {'u_id': 777, 'u_name': 'test', 'price_type_percent': False, 'price_val': '24980'}


redis_data1 = {'u_id': 111222333, 'u_name': 'VAlexandr', 'price_type_percent': False, 'price_val': '19500.01'}


async def add_user_subscription(connection, redis_data):
    if redis_data['price_type_percent'] is True:
        price = 1 - decimal.Decimal(redis_data['price_val'][:-1]) / 100
    else:
        price = decimal.Decimal(redis_data['price_val'])
    print(price)

    async with connection.transaction():
        await connection.execute(
            '''INSERT INTO users (user_id, name) VALUES ($1, $2) (user_id) 
            ON CONFLICT (user_id) DO UPDATE 
            SET btc_subscription=TRUE 
            WHERE users.btc_subscription=FALSE''',
            redis_data['u_id'], redis_data['u_name'])
        try:
            async with connection.transaction():
                print('nested tr')
                await connection.execute(
                    '''INSERT INTO users_subscriptions (user_id, price_type_percent, price_value)
                                        VALUES ($1, $2, $3)''',
                    redis_data['u_id'], redis_data['price_type_percent'], price)
                print('subscription added')
                return f'subscription added'
        except asyncpg.exceptions.UniqueViolationError:
            print('subs exists')
            return f'You have already had this subscription'


async def unsubscribe_all(connection, user_id):
    async with connection.transaction():
        await connection.execute(
            f'''UPDATE users SET btc_subscription=FALSE WHERE user_id=$1;''', user_id)
        print('unsubscribed')


async def show_subscriptions(connection, user_id):
    async with connection.transaction():
        subscribed = await connection.fetchrow('''SELECT "name", btc_subscription
                                                FROM users WHERE user_id = $1''', user_id)

        if subscribed['btc_subscription']:
            print(f'{subscribed["name"]}, you have a subscription')
            user_subscriptions = await connection.fetch('''
                SELECT id, price_type_percent, price_value FROM users_subscriptions 
                WHERE user_id=$1''', user_id)
            pprint(user_subscriptions)

        else:
            print(f'{subscribed["name"]}, no subscription')


async def remove_subscription(connection, subscriptions_ids):
    async with connection.transaction():
        await connection.execute('''DELETE FROM users_subscriptions WHERE id=any($1)''', subscriptions_ids)
        print('Subs deleted')


"""
# for add_u_subscr
async def main(data):
    con = await asyncpg.connect(host='localhost', database='test', user=db_user, password=db_passwd)
    u_subscr_task = asyncio.create_task(add_user_subscription(con, data))
    await u_subscr_task
    await asyncio.sleep(1)
    return u_subscr_task.result()
"""


async def main(u_data):
    con = await asyncpg.connect(host='localhost', database='test', user=db_user, password=db_passwd)
    u_subscr_task = asyncio.create_task(add_user_subscription(con, u_data))
    await u_subscr_task

    # unsubscr_task = asyncio.create_task(unsubscribe_all(con, 102))
    # await unsubscr_task

    # show_s_task = asyncio.create_task(show_subscriptions(con, 777))
    # await show_s_task

    # remove_task = asyncio.create_task(remove_subscription(con, [44, 46]))
    # await remove_task
    # await asyncio.sleep(1)

    # return u_subscr_task.result()


# asyncio.run(main())
