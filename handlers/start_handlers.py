from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from sdms_bot_creating import bot
from keyboards.main_menu_keyboard import main_menu
from keyboards.auth_menu_keyboard import auth_keyboard
from templates import notification


async def start(message: types.Message):  # Triggered on the first interaction
    await bot.send_message(message.from_user.id, notification.start_notification, reply_markup=auth_keyboard)


async def back(message: types.Message):
    await bot.send_message(message.from_user.id, notification.select_option, reply_markup=main_menu)


def start_register(dp: Dispatcher):  # Register of start_handler
    dp.register_message_handler(start, commands=['start', 'help', 'начать'])
    dp.register_message_handler(back, Text(equals="назад", ignore_case=True))


