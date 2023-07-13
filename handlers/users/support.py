from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from lib.db_changes import support_messages, create_ticket
from lib.db_selection import select_ticket_id
from loader import dp
from states import AdminSupport
from keyboards.inline import ikb_support, ikb_back
from utils.misc import rate_limit
from filters import delete_ikb


# Чат с админом
@dp.callback_query_handler(text='Support')
async def open_admin_chat(call: CallbackQuery):
    await create_ticket(user_id=call.from_user.id)  # создание тикета

    await call.message.edit_text('Ты попал в чатик с админом. Задай свой вопрос в следующем сообщении',
                                 reply_markup=ikb_back)

    await AdminSupport.support.set()  # устанавливаем состояние "support"


@rate_limit(limit=5)  # антиспам
# пока п-ль находится в состоянии "support" (при нажатой кнопке "Чат с админом"), отлавливать все сообщения
@dp.message_handler(state=AdminSupport.support)
async def add_message(message: types.Message):
    user_id = message.from_user.id
    ticket_id = await select_ticket_id(user_id)

    await support_messages(ticket_id, user_id, message.message_id, message.text)  # добавить сообщение в БД

    await delete_ikb(user_id, message.message_id)  # удалить предыдущую инлайн кнопку

    await message.reply(text='Сообщение отправлено👌', reply_markup=ikb_back)


# выход в главное меню (выход из состояния "support")
@dp.callback_query_handler(text='Back', state=AdminSupport.support)
async def send_message(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Заявка отменена⛔️😢', reply_markup=ikb_support)
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку

    await state.finish()
