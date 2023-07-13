import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from lib import db_changes, db_selection
from keyboards.inline import ikb_support, start_menu
from loader import dp
from states import Registration
from utils.misc import rate_limit


@rate_limit(limit=5)  # антиспам
@dp.message_handler(Command('start'))  # /start
async def user_register(message: types.Message):
    exist = await db_selection.exist_registration(message.from_user.id)

    if exist is True:
        await message.answer_animation(
            animation='CgACAgQAAxkBAAIVN2SlthgpebCfMl3Jc9w6rCp6VRcEAAI9AwACacEEU7o3VC5PLfGgLwQ',
            caption='Привет, я low_bot🙈. Чтобы узнать мою сущность, нажми на кнопку снизу⬇️',
            reply_markup=start_menu)
        # устанавливаем 1 состояние
        await Registration.login.set()
    else:
        if exist == 'created':
            await message.answer('Ты уже подал заявку🤝 Дождись решения🙄')
        elif exist == 'accepted':
            await message.answer('Ты уже зарегистрирован🥳')
        elif exist == 'cancelled':
            await message.answer('Заявка отменена⛔️😢', reply_markup=ikb_support)


@dp.callback_query_handler(text='регистрация', state=Registration.login)
async def get_login(call: CallbackQuery, state: FSMContext):
    await call.message.delete()  # удалить предыдущее сообщение

    fullname = call.from_user.first_name
    login = call.from_user.username

    if call.from_user.last_name is not None:  # если есть фамилия, добавить её к имени
        fullname += ' ' + call.from_user.last_name

    await db_changes.new_registration((str(call.from_user.id), login, fullname, 'created',
                                       str(datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")),))

    await call.message.answer(f'@{login}, ты подал заявку🫡 когда админ рассмотрит её, тебе придёт сообщение😇')

    await state.finish()
