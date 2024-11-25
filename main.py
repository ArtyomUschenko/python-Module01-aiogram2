from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold,italic,link
from aiogram.types import InputFile, MediaGroup
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
/photo - {italic('Концепция ЕИП ГосЭДО')}
/video - {italic('Информация о ГИС ТОСЭД')}
/voice - {italic('Голосовое сообщение')}
/group - {italic('Отправка пакета сообщений')}
/note - {italic('Отправка видеосообщений')}
/document - {italic('Отправка документа ПП198')}
/location- {italic('Отправка карту с адресом')}
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


#Отравка картинки пользователю
@dp.message_handler(commands=['photo'])
async def photo_command(message: types.Message):
    photo = InputFile("img/gosedo.png")
    # await bot.send_photo(message.from_user.id, photo="https://gosedo.ru/wp-content/uploads/2023/09/%D0%9A%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%86%D0%B8%D1%8F-%D0%95%D0%98%D0%9F-%D0%93%D0%BE%D1%81%D0%AD%D0%94%D0%9E.svg", caption="Концепция ЕИП ГосЭДО")
    await bot.send_photo(message.from_user.id, photo=photo, caption="Концепция ЕИП ГосЭДО")

#Отравка видео пользователю
@dp.message_handler(commands=['video'])
async def video_command(message: types.Message):
    video = InputFile("video/torsed.mp4") #Ограничение на размер файла в 50Mb от Telegram
    await bot.send_video(message.from_user.id, video=video, caption="Видео о ГИС ТОРСЭД")


@dp.message_handler(commands=['voice'])
async def voice_command(message: types.Message):
    voice = InputFile("audio/Планировщик задач.m4a")
    await bot.send_voice(message.from_user.id, voice=voice, caption="Голосовое сообщение")

@dp.message_handler(commands=['note'])
async def note_command(message: types.Message):
    note = InputFile("video/test.mp4")
    await bot.send_video_note(message.from_user.id, video_note=note)

@dp.message_handler(commands=['document'])
async def document_command(message: types.Message):
    document = InputFile("documents/ПП198.pdf")  #Отправка любого файла без сжатия
    await bot.send_document(message.from_user.id, document=document, caption="Постановление Правительства Российской Федерации от 17.02.2022 № 198")

@dp.message_handler(commands=['location'])
async def location_command(message: types.Message): #Отправка любого файла без сжатия
    await bot.send_location(message.from_user.id, latitude=55.683249, longitude=37.487397)
    await message.answer('улица Удальцова, 85, Москва, 119454')

@dp.message_handler(commands=['group'])
async def group_command(message: types.Message):
    media = MediaGroup()
    media.attach_photo(InputFile("img/Лого.png", "Логотип"))
    media.attach_photo(InputFile("img/gosedo.png", "Концепция ЕИП ГосЭДО"))
    await bot.send_media_group(message.from_user.id, media=media)


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


# 8