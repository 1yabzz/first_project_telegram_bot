from aiogram.utils import executor
from config import dp
from data_base import sqlite_db

async def on_startup(_):
    """пишет сообщение в консоль, когда запускаетсся бот и запускает бд"""
    print('Bot started')
    sqlite_db.sql_start()

from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)