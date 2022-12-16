"""кнопочуи админа"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# тексты запросов и ответов бота
from bot_text import *

button_load = KeyboardButton(LOAD_CMD)
button_delete = KeyboardButton('Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)