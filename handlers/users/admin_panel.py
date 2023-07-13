from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from aiogram.dispatcher.filters import Text

from filters import delete_ikb
from lib.config import admins
from lib import db_changes, db_selection
from loader import dp
from states import Accept, Cancel, Ticket
from keyboards.inline import (ikb_admin_main, ikb_admin_registration_user, ikb_support, ikb_back,
                              ikb_admin_show_tickets, ikb_admin_reply_to_ticket, ikb_admin_tickets_ids,
                              ikb_admin_show_messages, ikb_admin_reply, ikb_admin_sending_method,
                              ikb_admin_after_message_sent)


# админ панель
@dp.message_handler(text='/admin_panel', user_id=admins)
async def show_inline_menu(message: types.Message):
    await message.answer('☠️<b>Админка</b>☠️ | Выбери действие ниже.', reply_markup=ikb_admin_main)


# новые регистрации (новые пользователи)
@dp.callback_query_handler(text='Registrations')
async def get_registration(call: CallbackQuery):
    reg = await db_selection.select_registration()

    if reg is not None:
        await call.message.edit_text(f'<b>user_id:</b> <code>{reg[1]}</code>\n'
                                     f'<b>tg_login:</b> @{reg[2]}\n'
                                     f'<b>fullname:</b> {reg[3]}\n'
                                     f'<b>date_reg:</b> {reg[5]}\n', reply_markup=ikb_admin_registration_user)
    elif reg is None:
        await call.message.edit_text('Нет новых регистраций🙅‍♂️', reply_markup=ikb_back)


# подтверждение заявки (состояние: 1)
@dp.callback_query_handler(text='Accept')
async def accept_id(call: CallbackQuery):
    await call.message.answer('Введите id для подтверждения')
    await Accept.user_id.set()


# подтверждение заявки (завершить состояние)
@dp.message_handler(state=Accept.user_id, user_id=admins)
async def accept_reg(message: types.Message, state: FSMContext):
    await db_changes.accept_registration(message.text)
    await dp.bot.send_message(chat_id=message.text, text='Заявка принята✅🤗')  # отправить сообщение п-лю
    await message.answer('Подтверждён)')
    await state.finish()


# отклонение/отмена заявки (состояние: 1)
@dp.callback_query_handler(text='Cancel')
async def cancelled_id(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку
    await call.message.answer('Введите id для подтверждения')
    await Cancel.user_id.set()


# отклонение/отмена заявки (завершить состояние)
@dp.message_handler(state=Cancel.user_id, user_id=admins)
async def cancelled_reg(message: types.Message, state: FSMContext):
    await db_changes.cancelled_registration(message.text)
    await dp.bot.send_message(chat_id=message.text, text='Заявка отменена⛔️😢',
                              reply_markup=ikb_support)  # отправить сообщение пользователю
    await message.answer('Рассмотрено. Отказано. 😈')
    await state.finish()


# /admin_panel -> "Тикеты" >> количество тикетов
@dp.callback_query_handler(text='Тикеты')
async def get_tickets(call: CallbackQuery):
    count_tickets = len(await db_selection.new_tickets())

    if count_tickets == 0:
        reply_markup = ikb_back
    else:
        reply_markup = ikb_admin_show_tickets

    await call.message.edit_text(f'Новых тикетов: {count_tickets} шт.', reply_markup=reply_markup)


# /admin_panel -> "Тикеты" -> "Посмотреть" >> информация из тикетов: id/ticket_status/login/ticket_created_at
@dp.callback_query_handler(text='Посмотреть')
async def get_tickets(call: CallbackQuery):
    tickets_info = await db_selection.new_tickets()
    message_answer = ''
    for i in tickets_info:
        login = await db_selection.select_login(i[1])
        message_answer += f'<u>ticketID: {i[0]}</u> ({i[2]})\n' \
                          f'<b>login:</b> @{login}\n' \
                          f'<b>created_at:</b> {i[3]}\n\n' \

    await call.message.edit_text(message_answer, reply_markup=ikb_admin_reply_to_ticket)


# /admin_panel -> "Тикеты" -> "Посмотреть" -> "Ответить"  >> список из инлайн кнопок
@dp.callback_query_handler(text='Ответить')
async def get_tickets(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку
    tickets_ids = await db_selection.tickets_ids()
    await call.message.answer('Выбери id тикета, который возьмешь «в работу»',
                              reply_markup=ikb_admin_tickets_ids(tickets_ids))
    await Ticket.ticket.set()


# /admin_panel -> "Тикеты" -> "Посмотреть" -> "Ответить" -> Кнопка: id тикета >> вывод информации о тикете и п-ле
@dp.callback_query_handler(Text(startswith='ticket_'), state=Ticket.ticket)
async def get_tickets(call: CallbackQuery, state: FSMContext):
    ticket_id = call.data[7:]  # получить тикет id (число после "ticket_")
    user_id = await db_selection.select_user_id_by_ticket_id(ticket_id)

    async with state.proxy() as data:
        data['ticket_id'] = ticket_id
        data['user_id'] = user_id

    user_info = await db_selection.select_user_by_user_id(user_id)
    count_messages = len(await db_selection.select_messages_in_ticket(ticket_id))
    await call.message.edit_text(f'<u>ticketID: {ticket_id}</u>\n'
                                 f'<b>user_id:</b> {user_info[1]}\n'
                                 f'<b>login:</b> @{user_info[2]}\n'
                                 f'<b>name:</b> {user_info[3]}\n'
                                 f'<b>profile_status:</b> {user_info[4]}\n'
                                 f'<b>profile_created:</b> {user_info[5]}\n\n'
                                 f'Новых сообщений: {count_messages} шт.\n\n'
                                 f'Вывод: ⬇️',
                                 reply_markup=ikb_admin_show_messages)


# /admin_panel -> "Тикеты" -> "Посмотреть" -> "Ответить" -> Кнопка: id тикета -> "Показать сообщения" >>
# >> вывод сообщений из тикета текстом (1 сообщением)
@dp.callback_query_handler(text='Показать сообщения', state=Ticket.ticket)
async def get_tickets(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку

    data = await state.get_data()
    ticket_id = data.get('ticket_id')

    messages = await db_selection.select_messages_in_ticket(ticket_id)
    message_answer = ''

    if len(messages) == 0:
        message_answer = 'Нет новых сообщений'
    else:
        for row in messages:
            message_answer += f'<b>id:</b> <code>{row[0]}</code> <i>({row[5]})</i>\n' \
                              f'{row[4]}\n\n'
            # вывод в несколько сообщений (если символов в одном сообщении > 4096)
            if len(message_answer) > 4096:
                await call.message.answer(message_answer[:4096])
                message_answer = message_answer[4096:]

    await call.message.answer(message_answer, reply_markup=ikb_admin_reply)


# /admin_panel -> "Тикеты" -> "Посмотреть" -> "Ответить" -> Кнопка: id тикета -> "Показать сообщения" ->
# -> "Справка"
@dp.callback_query_handler(text='Справка', state=Ticket.ticket)
async def get_tickets(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку
    await call.message.answer(f'Чтобы ответить на конкретное сообщение, введи !<u>id сообщения</u> и '
                              f'свой текст с новой строки\n\n'
                              f'<i>Пример:</i>\n'
                              f'!105\n'
                              f'Какой-то текст\n\n'
                              f'Чтобы просто ответить, введи свой текст в следующем сообщении',
                              reply_markup=ikb_back)


# ввод текста сообщения для ответа пользователю
@dp.message_handler(state=Ticket.ticket, user_id=admins)
async def get_tickets(message: types.Message, state: FSMContext):
    await delete_ikb(message.from_user.id, message.message_id)  # удалить предыдущую инлайн кнопку
    await delete_ikb(message.from_user.id, message.message_id-1)  # удалить предыдущую инлайн кнопку

    message_text = message.text

    if message_text.startswith('!'):
        message_id = int(message_text.split()[0][1:])  # извлечь id (число после знака "!")

        # убрать из 1ой строки сообщения "!id"
        message_text = message_text.split('\n')[1:]
        message_text = '\n'.join(message_text)
        async with state.proxy() as data:
            data['message_id'] = message_id
            data['message_text'] = message_text

    else:
        async with state.proxy() as data:
            data['message_text'] = message_text

    await message.reply('Записал...', reply_markup=ikb_admin_sending_method)


# отправка сообщения или отмена отправки
@dp.callback_query_handler(text='Отправить', state=Ticket.ticket)
async def get_tickets(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку

    data = await state.get_data()

    message_text = f'<b>Сообщение от админа👮‍♂️:</b> \n\n'
    message_text += data.get('message_text')
    user_id = data.get('user_id')
    ticket_id = data.get('ticket_id')

    await db_changes.change_ticket_status(ticket_id=ticket_id, ticket_status='at_work')

    # если админ ввёл !id
    if 'message_id' in data:
        message_id_primary_key = data.get('message_id')
        message_id = await db_selection.select_message_id_by_id(message_id_primary_key)
        await dp.bot.send_message(chat_id=user_id, text=message_text, reply_to_message_id=message_id)

    else:
        await dp.bot.send_message(chat_id=user_id, text=message_text)

    await call.message.edit_text(f'<b>Сообщение отправлено</b>\n'
                                 f'{data}\n\n'
                                 f'Чтобы <u>отправить ещё</u>, введи свой текст в следующем сообщении',
                                 reply_markup=ikb_admin_after_message_sent)


# /admin_panel -> "Тикеты" -> "Посмотреть" -> "Ответить" -> Кнопка: id тикета -> "Показать сообщения" ->
# -> Текст сообщения -> "Отправить" -> "Закрыть тикет"
@dp.callback_query_handler(text='Закрыть тикет', state=Ticket.ticket, user_id=admins)
async def send_message(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get('ticket_id')

    await db_changes.change_ticket_status(ticket_id=ticket_id, ticket_status='closed')

    await call.message.edit_text(f'<b>Сообщение отправлено</b>\n'
                                 f'{data}\n\n'
                                 f'<u>Тикет закрыт</u>',
                                 reply_markup=ikb_back)

    await state.finish()


# назад + завершить состояние (кнопка "назад" >> /admin_panel)
@dp.callback_query_handler(text='Back', state=Ticket.ticket, user_id=admins)
async def send_message(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку
    await call.message.answer('☠️<b>Админка</b>☠️ | Выбери действие ниже.', reply_markup=ikb_admin_main)
    await state.finish()


# кнопка "назад" >> /admin_panel
@dp.callback_query_handler(text='Back', user_id=admins)
async def send_message(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)  # удалить предыдущую инлайн кнопку
    await call.message.answer('☠️<b>Админка</b>☠️ | Выбери действие ниже.', reply_markup=ikb_admin_main)


# кнопка "Отмена отправки" + завершить состояние >> /admin_panel
@dp.callback_query_handler(text='Отмена отправки', state=Ticket.ticket, user_id=admins)
async def send_message(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Отмена отправки')
    await call.message.answer('☠️<b>Админка</b>☠️ | Выбери действие ниже.', reply_markup=ikb_admin_main)
    await state.finish()
