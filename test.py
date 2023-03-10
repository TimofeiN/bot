import asyncio
import unittest
import aiohttp
from unittest import IsolatedAsyncioTestCase

import db_functions as db
from main import bot
from app.binance_req import current

# import config
# from database import cache, database


test_data = {'u_id': 111, 'u_name': 'test', 'price_type_percent': False, 'price_val': '11122.33'}
# u_subs = {106: 'price value 1234.56$', 104: 'price value 10.00%', 105: 'price value 15000.00$'}


class TestDatabase(IsolatedAsyncioTestCase):
    async def test_db(self):
        await db.db_main(db.add_user_subscription, test_data)
        self.assertEqual(await db.db_main(db.check_subscribed, test_data['u_id']), True)
        await db.db_main(db.unsubscribe_all, test_data['u_id'])
        self.assertEqual(await db.db_main(db.check_subscribed, test_data['u_id']), False)


class TestBot(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = bot
        self.bot._session = aiohttp.ClientSession()

    async def test_bot_auth(self):
        bot_task = asyncio.create_task(self.bot.get_me())
        await bot_task
        await asyncio.sleep(0)
        bot_info = bot_task.result()
        self.assertEqual(bot_info["username"], "kartuli_ghvino_bot")

    async def asyncTearDown(self):
        await self.bot._session.close()


class TestApi(IsolatedAsyncioTestCase):
    async def test_response(self):
        task = asyncio.create_task(current('BTCUSDT'))
        await task
        result = task.result()
        self.assertNotEqual(result, None)


if __name__ == '__main__':
    unittest.main()
