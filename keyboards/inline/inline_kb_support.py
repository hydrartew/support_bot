from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_support = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Чат с админом', callback_data='Support')
                                    ]
                                    ])
