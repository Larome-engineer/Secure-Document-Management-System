from aiogram import Bot, Dispatcher
from templates import variables
from aiogram.contrib.fsm_storage.memory import MemoryStorage


memory = MemoryStorage()
bot = Bot(variables.bot_token)
dispatcher = Dispatcher(bot, storage=memory)
