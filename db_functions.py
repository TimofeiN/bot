import asyncio
import asyncpg
import decimal
# from pprint import pprint

from back.xconfig import db_user, db_passwd


async def add_user_subscription(connection, redis_data):
    if redis_data['price_type_percent'] is True:
        price = 1 - decimal.Decimal(redis_data['price_val'][:-1]) / 100
    else:
        price = decimal.Decimal(redis_data['price_val'])
    print(price)

    async with connection.transaction():
        await connection.execute(
            '''INSERT INTO users (user_id, name) VALUES ($1, $2) 
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
                return f'Subscription added'
        except asyncpg.exceptions.UniqueViolationError:
            print('subs exists')
            return f'You have already had this subscription'


async def unsubscribe_all(connection, user_id):
    async with connection.transaction():
        await connection.execute(
            f'''UPDATE users SET btc_subscription=FALSE WHERE user_id=$1;''', user_id)
        await connection.execute(
            '''DELETE FROM users_subscriptions WHERE user_id=$1''', user_id)

        return f'unsubscribed'


async def show_subscriptions(connection, user_id):
    async with connection.transaction():
        subscribed = await connection.fetchrow('''SELECT btc_subscription
                                                FROM users WHERE user_id = $1''', user_id)

        if subscribed['btc_subscription']:
            # print(f'you have a subscriptions:')
            user_subscriptions = {}
            async for record in connection.cursor(f'''
                    SELECT id, price_type_percent, price_value FROM users_subscriptions 
                    WHERE user_id=$1''', user_id):
                sub_id = record['id']
                percent = record['price_type_percent']
                if percent:
                    u_price = (1 - record['price_value']) * 100
                    symbol = '%'
                else:
                    u_price = record['price_value']
                    symbol = '$'
                # user_subscriptions += emoji.emojize(f':incoming_envelope: {sub_id}:  price value {u_price}{symbol}\n')
                subscription = {sub_id: f'price value {u_price}{symbol}'}
                user_subscriptions.update(subscription)

            # print(user_subscriptions)
            return user_subscriptions


async def remove_subscription(connection, subscriptions_ids):
    async with connection.transaction():
        await connection.execute('''DELETE FROM users_subscriptions WHERE id=any($1)''', subscriptions_ids)
        print('Subs deleted')
        return f'Subscriptions changed'


async def db_main(db_function, u_data):
    con = await asyncpg.connect(host='localhost', database='test', user=db_user, password=db_passwd)

    db_task = asyncio.create_task(db_function(con, u_data))
    await db_task
    await asyncio.sleep(1)
    return db_task.result()

    # u_subscr_task = asyncio.create_task(add_user_subscription(con, u_data))
    # await u_subscr_task
    # await asyncio.sleep(1)
    # return u_subscr_task.result()

    # unsubscr_task = asyncio.create_task(unsubscribe_all(con, 102))
    # await unsubscr_task

    # show_s_task = asyncio.create_task(show_subscriptions(con, 777))
    # await show_s_task

    # remove_task = asyncio.create_task(remove_subscription(con, u_data))
    # await remove_task
    # await asyncio.sleep(1)

    # return u_subscr_task.result()


# print(asyncio.run(db_main(add_user_subscription, redis_data1)))
