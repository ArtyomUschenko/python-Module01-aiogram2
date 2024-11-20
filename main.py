from aiogram import Bot, Dispatcher, executor, types
import api_token

bot = Bot(api_token.TOKEN) # токен
dp = Dispatcher(bot) # диспетчер

HELP_TEXT   = '''
/help - помощь
/start - запуск бота
'''


@dp.message_handler(commands=['help']) # команда /help
async def help_command(message: types.Message):
    await message.answer(HELP_TEXT)

@dp.message_handler(commands=['start']) # команда /start
async def start_command(message: types.Message):
    await message.reply('Привет, я бот, который может проконсультировать тебя о системе.')


#Уведомление о запуске бота
async def on_startup(_):
    print('Бот был успешно перезапущен!')

# Функция эхо, повторяет все сообщения пользователя
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(f"Привет, {message.chat.first_name}!\n\nЕсли нужна помощь, то введи команду /help")
    print(message)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
