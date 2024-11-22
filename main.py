from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold,italic,link
import api_token

bot = Bot(api_token.TOKEN) # токен
dp = Dispatcher(bot) # диспетчер



# Вариант с поддержкой HTML
# --------------------------------------------------
# HELP_TEXT   = '''
# /help - <b> помощь </b>
# /start - <i> запуск бота </i>
# '''
#
# @dp.message_handler(commands=['help']) # команда /help
# async def help_command(message: types.Message):
#     await message.answer(HELP_TEXT, parse_mode="HTML")  #parse_mode="HTML" - вывод в HTML


# Вариант с поддержкой markdown
# --------------------------------------------------
HELP_TEXT   = f'''
/help - {bold('помощь')}
/start - {italic('запуск бота')}
/sticker - {italic('Тест')}
 {link("ГИС ГосЭДО",'https://gosedo.ru/')} - {italic('официальный сайт')}

'''

@dp.message_handler(commands=['help']) # команда /help
async def help_command(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode="markdown")  #parse_mode="markdown" - вывод в markdown


@dp.message_handler(commands=['help']) # команда /help
async def help_command(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode="HTML")  #parse_mode="HTML" - вывод в HTML


@dp.message_handler(commands=['start']) # команда /start
async def start_command(message: types.Message):
    await message.reply('Привет, я бот, который может проконсультировать тебя о системе. 😅')


# Отправка стикера пользователю
@dp.message_handler(commands=['sticker']) # команда /sticker
async def sticker_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAENLhBnPhNSct_FCoK6HrLHzzMp8f69ogACAQEAAladvQoivp8OuMLmNDYE")

#Уведомление о запуске бота
async def on_startup(_):
    print('Бот был успешно перезапущен! 😅')

# Функция эхо, повторяет все сообщения пользователя
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n\nЕсли нужна помощь, то введи команду /help")
    print(message)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


# 4