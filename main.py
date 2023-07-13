from aiogram import executor

import middlewares
from lib import db
from handlers import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    middlewares.setup(dp)
    await on_startup_notify(dp)
    await set_default_commands(dp)
    await db.create_table_user()
    await db.create_table_messages()
    await db.create_table_tickets()
    print('Бот запущен!')
    

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
