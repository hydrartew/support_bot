from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    login = State()


class Accept(StatesGroup):
    user_id = State()


class Cancel(StatesGroup):
    user_id = State()


class AdminSupport(StatesGroup):
    support = State()


class Ticket(StatesGroup):
    ticket = State()
