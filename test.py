# импорт всего необходимого
import asyncio
from aiogram import executor, types
import unittest
from unittest import TestCase
from unittest.mock import patch

# импорт текстов запросов и ответов бота
from bot_text import *

# импорт обработчиков 
from handlers import client, admin, other

# импорт обработчика клиента 
from handlers.client import *
from handlers.other import *

from bot_text import *

# тексты запросов
req_cmd = ['not defined', START_CMD, HISTORY_CMD, PLACE_CMD, QUESTIONS_CMD]
# тексты ответов
bot_ans = [GREETING_ANS, GREETING_ANS, HISTORY_ANS, PLACE_ANS, QUESTIONS_ANS]

class TestBot(TestCase):

    # Тестирует правильность обработки сценария, происходит проверка 
    # на количество ответов требуемому и что ответы соответствуют ожидаемым
    def test_scenario(self):
        # патчим, чтобы все сообщения бота собирались в send_messages 
        with patch('aiogram.bot.Bot.send_message', return_value = None) as send_messages:
            # тестируем команду, которую бот не знает
            message_mock =  unittest.mock.Mock(text = "not defined")
            asyncio.run(bad_command(message_mock))
            # тестируем команду /start
            message_mock = unittest.mock.Mock(text = START_CMD)
            asyncio.run(command_start(message_mock))
            # тестируем команду "Наша история"
            message_mock = unittest.mock.Mock(text = HISTORY_CMD)
            asyncio.run(history_command(message_mock))
            # тестируем команду "Расположение"
            message_mock = unittest.mock.Mock(text = PLACE_CMD)
            asyncio.run(place_command(message_mock))
            # тестируем команду "Часто задаваемые вопросы"
            message_mock = unittest.mock.Mock(text = QUESTIONS_CMD)
            asyncio.run(questions_command(message_mock))

        # здесь соберем все ответы бота
        test_ans = []
        # цикл по принятым сообщениям
        for args, kwargs in send_messages.call_args_list:
            test_ans.append(args[1])
        # проверка, что количество ответов бота сообветствует заданному 
        # ошибка, если количество не совпадает
        self.assertEqual(len(test_ans), len(bot_ans)) 
        # проверка ответов бота
        for t_ans, b_ans in zip(test_ans, bot_ans):
            # ошибка, если ответ не совпадает
            self.assertEqual(t_ans, b_ans) 

if __name__ == '__main__':
    print('Test Bot started')
    unittest.main()
