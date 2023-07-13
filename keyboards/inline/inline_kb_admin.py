from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_admin_main = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Список рег-ий', callback_data='Registrations'),
        InlineKeyboardButton(text='Тикеты', callback_data='Тикеты'),
    ]
])


ikb_admin_registration_user = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Accept✅', callback_data='Accept'),
        InlineKeyboardButton(text='Cancel❌', callback_data='Cancel'),
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='Back'),
    ],
])


ikb_admin_show_tickets = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Посмотреть', callback_data='Посмотреть'),
        InlineKeyboardButton(text='Назад', callback_data='Back'),
    ]
])


ikb_admin_reply_to_ticket = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Ответить', callback_data='Ответить'),
        InlineKeyboardButton(text='Назад', callback_data='Back'),
    ]
])


def ikb_admin_tickets_ids(tickets: list):
    kb = InlineKeyboardMarkup(row_width=3)
    for item in tickets:
        kb.insert(InlineKeyboardButton(text=item, callback_data=f'ticket_{item}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='Back'))
    return kb


ikb_admin_show_messages = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Показать сообщения', callback_data='Показать сообщения'),
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='Back'),
    ],
])


ikb_admin_reply = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Справка', callback_data='Справка'),
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='Back'),
    ],
])


ikb_admin_sending_method = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отправить', callback_data='Отправить'),
    ],
    [
        InlineKeyboardButton(text='Отмена отправки', callback_data='Отмена отправки'),
    ],
])


ikb_admin_after_message_sent = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Закрыть тикет', callback_data='Закрыть тикет'),
        InlineKeyboardButton(text='Вернуться в админку', callback_data='Back'),
    ],
])
