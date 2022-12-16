from aiogram import types, Dispatcher
from config import bot, dp

# тексты запросов и ответов бота
from bot_text import *


async def bad_command(message: types.Message):
    """обработка сценария вне команд бота"""
    await bot.send_message(message.from_user.id, GREETING_ANS)

def register_handlers_other(dp: Dispatcher):
    """регистрация хендлера"""
    dp.register_message_handler(bad_command)