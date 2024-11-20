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



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)