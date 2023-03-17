import asyncio
import asyncpg
import decimal

from back.xconfig import db_user, db_passwd, db_name


# add user option to database used cache Redis FSM
async def add_user_subscription(connection, redis_data):
    if redis_data['price_type_percent'] is True:
        price = 1 - decimal.Decimal(redis_data['price_val'][:-1]) / 100
    else:
        price = decimal.Decimal(redis_data['price_val'])

    async with connection.transaction():
        await connection.execute(
            '''INSERT INTO users (user_id, name) VALUES ($1, $2) 
            ON CONFLICT (user_id) DO UPDATE 
            SET btc_subscription=TRUE 
            WHERE users.btc_subscription=FALSE''',
            redis_data['u_id'], redis_data['u_name'])
        try:
            async with connection.transaction():
                await connection.execute(
                    '''INSERT INTO users_subscriptions (user_id, price_type_percent, price_value)
                                        VALUES ($1, $2, $3)''',
                    redis_data['u_id'], redis_data['price_type_percent'], price)
                return f'Subscription added'
        except asyncpg.exceptions.UniqueViolationError:
            return f'You have already had this subscription'


# Remove all users options from database
async def unsubscribe_all(connection, user_id):
    async with connection.transaction():
        await connection.execute(
            f'''UPDATE users SET btc_subscription=FALSE WHERE user_id=$1;''', user_id)
        await connection.execute(
            '''DELETE FROM users_subscriptions WHERE user_id=$1''', user_id)

        return f'unsubscribed'


# Take all user options from database
async def show_subscriptions(connection, user_id):
    async with connection.transaction():
        subscribed = await connection.fetchrow('''SELECT btc_subscription
                                                FROM users WHERE user_id = $1''', user_id)

        if subscribed['btc_subscription']:
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
                subscription = {sub_id: f'price value {u_price}{symbol}'}
                user_subscriptions.update(subscription)
            return user_subscriptions


# Remove some rows from database
async def remove_subscription(connection, subscriptions_ids):
    async with connection.transaction():
        await connection.execute('''DELETE FROM users_subscriptions WHERE id=any($1)''', subscriptions_ids)
        return f'Subscriptions changed'


async def check_subscribed(connection, user_id):
    async with connection.transaction():
        response = await connection.fetchrow('''SELECT btc_subscription FROM users WHERE user_id = $1''', user_id)
        value = response['btc_subscription']
        return value


# Remove all user's data from database
async def delete_user(connection, user_id):
    async with connection.transaction():
        await connection.execute('''DELETE FROM users_subscriptions WHERE user_id=$1''', user_id)
        await connection.execute('''DELETE FROM users WHERE user_id=$1''', user_id)


# Main coroutine for database
async def db_main(db_function, u_data):
    con = await asyncpg.connect(host='localhost', database=db_name, user=db_user, password=db_passwd)

    db_task = asyncio.create_task(db_function(con, u_data))
    await db_task
    await asyncio.sleep(1)
    return db_task.result()
