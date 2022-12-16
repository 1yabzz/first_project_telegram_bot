import sqlite3 as sq
from config import bot,dp

#подкючаем или создаем файл базы данных, создаем курсор,создаем таблицу если такой не существует 
def sql_start():
    global base, cur
    base = sq.connect('sistem_adm.dp')
    cur = base.cursor()
    if base:
        print('Data base connected sessions OK!')
    base.execute('CREATE TABLE IF NOT EXISTS sessions(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')#img c text потому что фотка сохраняется по айдишнику
    base.commit()
#записываем изменения в базу данных заполняем таблицу с помощью execute и сохраняем
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO sessions VALUES (?,?,?,?)', tuple(data.values()))#перевод в кортеж 
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM sessions').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'Администратор: {ret[1]}\n\nИнформация о сотруднике: {ret[2]}\n\nВремя сессии:{ret[3]}')

async def sql_read2():
    return cur.execute ('SELECT * FROM sessions').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM sessions WHERE name == ?', (data,))
    base.commit()
