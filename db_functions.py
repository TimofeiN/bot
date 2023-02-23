import asyncio
import asyncpg
import decimal
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
            '''INSERT INTO users (user_id, name) VALUES ($1, $2) ON CONFLICT DO NOTHING''',
            redis_data['u_id'], redis_data['u_name'])
        print('user added')
        try:
            async with connection.transaction():
                print('nested tr')
                await connection.execute(
                    '''INSERT INTO users_subscriptions (user_id, price_type_percent, price_value)
                                        VALUES ($1, $2, $3)''',
                    redis_data['u_id'], redis_data['price_type_percent'], price)
                print('subscription added')
        except asyncpg.exceptions.UniqueViolationError:
            print('subs exists')
            return f'You have already had this subscription'


async def main(data):
    con = await asyncpg.connect(host='localhost', database='test', user=db_user, password=db_passwd)
    u_subscr_task = asyncio.create_task(add_user_subscription(con, data))
    await u_subscr_task
    await asyncio.sleep(1)
    return u_subscr_task.result()


# asyncio.run(main(redis_data1))
