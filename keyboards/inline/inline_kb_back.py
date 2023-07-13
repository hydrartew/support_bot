from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_back = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Назад', callback_data='Back')
                                    ]
                                    ])
