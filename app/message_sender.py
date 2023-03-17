import asyncpg
import asyncio
import logging
from aiogram import Bot


from back.xconfig import db_user, db_passwd
from app.binance_req import current
from app.messages import msg


# Main background function iterates throw database records and send message to user
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

            if cur_price['current_price'] < user_price:
                current_price = round(cur_price['current_price'], 4)
                profit = user_price - cur_price['current_price']
                logging.info(f'   --> sending msg to user_id #{user_id}')
                text = msg.price_drop.format(current_price=current_price, profit=profit)
                bot = Bot.get_current()
                await bot.send_message(chat_id=user_id, text=text)


async def message_sender():
    while True:
        task = asyncio.create_task(iterate())
        await task
        # print('sleep')
        await asyncio.sleep(10)
