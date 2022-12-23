from DAO import person_dao
from sdms_bot_creating import bot
from templates import notification
from keyboards import auth_keyboard
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards.main_menu_keyboard import main_menu

whitelist = {}


async def authorization(message: types.Message):  # Check of exists in DB and then authorizes the user or send for reg
    post = person_dao.search_post_by_tg_id(message.from_user.id)

    if post is None:
        await bot.send_message(message.from_user.id, notification.not_in_db_notification)

    elif post is not None:
        whitelist[message.from_user.id] = post
        await bot.send_message(message.from_user.id, notification.auto_auth_notification, reply_markup=main_menu)


async def logout(message: types.Message):  # Logout method
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.not_log_notification)
    else:
        whitelist.pop(message.from_user.id)
        await bot.send_message(message.from_user.id, notification.logout_notification, reply_markup=auth_keyboard)


def auth_register(dp: Dispatcher):  # Register of auth_handlers

    dp.register_message_handler(authorization, Text(equals='авторизация', ignore_case=True), state=None)
    dp.register_message_handler(logout, Text(equals='выйти', ignore_case=True))




