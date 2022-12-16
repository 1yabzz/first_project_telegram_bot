from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# тексты запросов и ответов бота
from bot_text import *

b1 = KeyboardButton(HISTORY_CMD)
b2 = KeyboardButton(PLACE_CMD)
b3 = KeyboardButton(QUESTIONS_CMD)
b4 = KeyboardButton(ENROLL_CMD)

kb_client= ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4)