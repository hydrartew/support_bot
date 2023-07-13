from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from lib import config

# переменная бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# хранение в ОП
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
