from aiogram import types, Dispatcher
from config import bot, dp
from keyboards import kb_client 
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

# тексты запросов и ответов бота
from bot_text import *

ADMINS_ID = 1760676377

kb = InlineKeyboardMarkup(row_width=2)
Button = InlineKeyboardButton(text='Записаться на сессию самокат', callback_data='самокат')
Button2 = InlineKeyboardButton(text='Записаться на сессию BMX', callback_data='велосипед')
kb.row(Button).row(Button2)


@dp.message_handler(text=[START_CMD])
async def command_start(message: types.Message):
    """принимает в себя сообщение и отправляет ответ"""
    await bot.send_message(message.from_user.id, GREETING_ANS, reply_markup=kb_client)

@dp.message_handler(text=[HISTORY_CMD])
async def history_command(message: types.Message):
    """принимает в себя сообщение и отправляет ответ"""
    await bot.send_message(message.from_user.id, HISTORY_ANS)

@dp.message_handler(text=[PLACE_CMD])
async def place_command(message: types.Message):
    """принимает в себя сообщение и отправляет ответ"""
    await bot.send_message(message.from_user.id, PLACE_ANS)

@dp.message_handler(text=[QUESTIONS_CMD])
async def questions_command(message: types.Message):
    """принимает в себя сообщение и отправляет ответ"""
    await bot.send_message(message.from_user.id, QUESTIONS_ANS)

@dp.message_handler(text=[ENROLL_CMD])
async def enroll_command(message: types.Message):
    """принимает в себя сообщение и отправляет все возможные сессии"""
    read = await sqlite_db.sql_read2()
    for cat in read:
        await bot.send_photo(message.from_user.id, cat[0], f'{cat[1]}\n Информация: {cat[2]} \n Время: {cat[3]}')
        await bot.send_message(message.from_user.id, text=ENROLL_ANS, reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton(text='записаться в это время и день', callback_data=f'день {cat[2]} время {cat[3]}' )))

@dp.callback_query_handler(Text(startswith='день '))
async def w_day(callback: types.CallbackQuery):
    """отправляет сообщение админу с днем записи и временем"""
    res = callback.data
    await bot.send_message(ADMINS_ID,f'{res}')



def register_handlers_client(dp: Dispatcher):
    """регистрация хендлера"""
    dp.register_message_handler (command_start, commands=['start','help'])
    dp.register_message_handler (history_command, text=HISTORY_CMD)
    dp.register_message_handler (place_command, text=PLACE_CMD)
    dp.register_message_handler (questions_command, text=QUESTIONS_CMD)
    dp.register_message_handler (enroll_command, text=ENROLL_CMD)