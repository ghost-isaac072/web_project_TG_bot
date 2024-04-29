from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup # Необходимы для
from aiogram.fsm.context import FSMContext # Для добавления состояний

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()


@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в https://t.me/oskalmanSHOP', reply_markup=kb.main)
    # await message.reply('Как дела?')
    # message.reply - ответ на сообщение пользователя
    # с выделением его сообщения

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('@OSKALMAN_1 - по вопросам о товарах\n'
                         '@Ghost_Isaac072 - по вопросам о работе бота')


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.message(F.text == 'О нас')
async def abour_us(message: Message):
    await message.answer('Мы - самые лучшие и надёжные продавцы импортной одежды в РФ\n'
                         '@OSKALMAN_1 - по вопросам о товарах\n'
                         '@Ghost_Isaac072 - по вопросам о работе бота'
                         )


@router.message(F.text == 'Контакты')
async def abour_us(message: Message):
    await message.answer('@OSKALMAN_1 - по вопросам о товарах\n'
                         '@Ghost_Isaac072 - по вопросам о работе бота'
                         )


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выбери товар',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\n'
                                  f'Описание: {item_data.description}\n'
                                  f'Цена: {item_data.price}₽',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))




# @router.message(F.text == 'Каталог')
#async def nice(message: Message):
 #   await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


#@router.callback_query(F.data == 't-shirt')
#async def t_shirt(callback: CallbackQuery):
 #   await callback.answer('Вы выбрали категорию')
    # show_alert=True - делает уведомление более "навязчивым":
    # всплывает отдельное окно с уведомлением
  #  await callback.message.answer('Вы выбрали категорию футболок')


#@router.message(Command('register'))
#async def register(message: Message, state: FSMContext):
#    await state.set_state(Register.name)
#    await message.answer('Введите ваше имя')


#@router.message(Register.name)
#async def register_name(message: Message, state: FSMContext):
#    await state.update_data(name=message.text)
#    await state.set_state(Register.age)
#    await message.answer('Введите ваш возраст')


#@router.message(Register.age)
#async def register_age(message: Message, state: FSMContext):
#    await state.update_data(age=message.text)
#    await state.set_state(Register.number)
#    await message.answer('Отправьте Ваш номер телефона', reply_markup=kb.get_number)


#@router.message(Register.number, F.contact)
#async def register_number(message: Message, state: FSMContext):
#    await state.update_data(number='+' + message.contact.phone_number)
#    data = await state.get_data()
#    await message.answer(f"Ваше имя: {data['name']}\nВаш возраст: {data['age']}\nВаш номер: {data['number']}")
#    await state.clear()