from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_cb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# тексты запросов и ответов бота
from bot_text import *

ADMIN_ID = {'руслан' : 1760676377, 'kenbk': 14354634654, 'eglghitnhtnht4':434654765}
MAIN_ADMIN = 1760676377

valyok = ''
keyok = ''

class FSMadmin2(StatesGroup):
    adminname = State()
    idi = State()


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    info = State()
    time = State()


async def make_changes_command(message: types.Message):
    """ функция принимает в себя команду moderator 
    и отправляет ответ """
    global MAIN_ADMIN
    await bot.send_message(message.from_user.id, 'какие хотите добавить обновления?',reply_markup=admin_cb.button_case_admin)

async def cm_start(message: types.Message):
    """ функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, запускает машину состояний
    и отправляет сообщение"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        await FSMadmin.photo.set()
        await message.reply(LOAD_ANS)

async def load_photo(message: types.Message, state: FSMContext):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, сохраняет в себя отправленное ранее фото, переключает состояние машины состояний 
    и отправляет сообщение"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи имя администратора')

async def load_name(message: types.Message, state:FSMContext):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, сохраняет в себя отправленное ранее имя администратора , переключает состояние машины состояний 
    и отправляет сообщение"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('Теперь введи информацию об администраторе')

async def load_info(message: types.Message, state:FSMContext):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, сохраняет в себя отправленную ранее информацию об админе, переключает состояние машины состояний 
    и отправляет сообщение"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['info'] = message.text
        await FSMadmin.next()
        await message.reply('Теперь введи время работы администратора')

async def load_time(message: types.Message, state:FSMContext):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, сохраняет в себя отправленное ранее время, завершает работу машины состояний и сохраняет результат в базу данных"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['time'] = message.text
        await sqlite_db.sql_add_command(state)

        await state.finish()

async def cancel_handlers_admin(message: types.Message, state: FSMContext):
    """функция принимает в себя сообщение,а именно команду отмена, проверяет айди человека со списком админов,
    если совпадает, то заканчивает работу машины состояний"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    """удаляет запись из базы данных и отправляет сообщение"""
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалена.', show_alert=True)


async def delete_item(message: types.Message):
    """принимает запрос на удаление сессии и выводит все возможные сессии с инлайн клавиатурой"""
    if message.from_user.id in ADMIN_ID.values() or message.from_user.id == MAIN_ADMIN:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Информация: {ret[2]} \n Время: {ret[3]}')
            await bot.send_message(message.from_user.id, text='Вы хотите удалить эту запись ^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}',callback_data=f'del {ret[1]}')))


@dp.message_handler(commands='newadmin')
async def phrase1(message: types.Message):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, запускает машину состояний и отправяет сообщение"""
    if message.from_user.id == MAIN_ADMIN:
        await FSMadmin2.adminname.set()
        await bot.send_message(message.from_user.id,'Введите имя администратора')

@dp.message_handler(state=FSMadmin2.adminname)
async def load_adminname(message: types.Message, state:FSMContext):
    """функция принимает в себя сообщение, проверяет айди человека со списком админов,
    если совпадает, сохраняет в себя отправленное имя"""
    if message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['adminname'] = message.text
        global keyok
        keyok = message.text
        await FSMadmin2.next()
        await message.reply('введи айди админа без посторонних символов и даже пробелов')

@dp.message_handler(state=FSMadmin2.idi)
async def load_idi(message: types.Message, state:FSMContext):
    """функция проверяет айди отправителя, закидывает в словарь айди с именем и завершает машину состояний"""
    if message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['idi'] = message.text
        valyok = message.text
        ADMIN_ID[keyok] = valyok
        await state.finish()
        await message.reply('админ успешно сохранен')

@dp.message_handler(commands='deladmin')
async def koks(message: types.Message):
    """отправляет все возможные имена и айдишники с инлайн клавиатурой"""
    if message.from_user.id == MAIN_ADMIN:
        for key,values in ADMIN_ID.items():
            await bot.send_message(message.from_user.id, f'имя:{key}\nайди:{values}',reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton(text='удалить админмистратора', callback_data=f'удалить {key}')))

@dp.callback_query_handler(Text(startswith='удалить '))
async def deleted(callback: types.CallbackQuery):
    """удаляет item из словаря"""
    result = callback.data.split('удалить ')
    result1 = result[1]
    for zet,val in ADMIN_ID.items():
        if str(result1) == str(zet):
            ADMIN_ID.pop(result1)
            await bot.send_message(MAIN_ADMIN, 'админ успешно удален')
            break


@dp.message_handler(state='*',commands='отмена')
@dp.message_handler(Text(equals = 'отмена', ignore_case=True),state='*')
async def cancel_handlers(message: types.Message, state: FSMContext):
    """завершает машину состояний по команде"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

def register_handlers_admin(dp: Dispatcher):
    """регистрация хендлеров"""
    dp.register_message_handler(make_changes_command, commands=['moderator'] )
    dp.register_message_handler(cm_start, text=LOAD_CMD, state=None)
    dp.register_message_handler(load_photo, content_types=['photo'],state=FSMadmin.photo)
    dp.register_message_handler(load_name,state=FSMadmin.name)
    dp.register_message_handler(load_info,state=FSMadmin.info)
    dp.register_message_handler(load_time,state=FSMadmin.time)
    dp.register_message_handler(delete_item, text='Удалить')