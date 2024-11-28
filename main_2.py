
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from babel.plural import skip_token
import asyncio

import api_token
from sqlite_db import db_start, create_profile, edit_profile

# Анкета пользователя
# ---------------------------------------------------------------


storage = MemoryStorage() # локальное хранилище
bot = Bot(api_token.TOKEN) # токен
dp = Dispatcher(bot,storage=storage) # диспетчер

class ProfileStates(StatesGroup):
    name = State()
    age = State()
    description = State()
    photo = State()



#
@dp.message_handler(commands=['start']) # команда /start
async def start_command(message: types.Message):
    await message.answer("Привет, я бот, который может проконсультировать тебя о системе. 😅 Для регистрации введите команду /create ")
    await create_profile(user_id=message.from_user.id)


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply("Отправка заявки прервана")




@dp.message_handler(commands=['create']) # команда /create
async def create_command(message: types.Message):
    await message.answer( "Пришлите ваше имя ")
    await ProfileStates.name.set()

@dp.message_handler(state=ProfileStates.name)
async def checking_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer( "Пришлите ваш возраст ")
    await ProfileStates.next()

#Проверка ввода цифр в раздел возраст
@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStates.age)
async def checking_input_age(message: types.Message):
    return await message.reply("Введите число")

@dp.message_handler(state=ProfileStates.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer( "Пришлите комментарий")
    await ProfileStates.next()


@dp.message_handler(state=ProfileStates.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.answer( "Пришлите изображение")
    await ProfileStates.next()

@dp.message_handler(lambda message: not message.photo or len(message.photo) == 0, state=ProfileStates.photo)
async def checking_input_photo(message: types.Message):
    await message.reply("Отправьте изображение")


@dp.message_handler(content_types=["photo"], state=ProfileStates.photo)
async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(message.from_user.id, photo=data['photo'], caption=f'{data["name"]}, {data["age"]}, {data["description"]}')
    await edit_profile(state, user_id=message.from_user.id)
    await message.answer( "Ваше сообщение отправлено")
    await state.finish() # завершаем состояни


async def on_startup(_):
    await db_start()
    print("Подключение к БД выполнено")



if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)


#