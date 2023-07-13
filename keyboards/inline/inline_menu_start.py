from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_menu = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Зарегистрироваться', callback_data='регистрация'),
                                      ],
                                  ],
                                  one_time_keyboard=True
                                  )
