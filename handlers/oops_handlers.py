from aiogram import types, Dispatcher
from sdms_bot_creating import bot
from templates import notification


async def oops(message: types.Message):  # Catches all unknown messages
    await bot.send_message(message.from_user.id, notification.d_understand_notification)


def oops_register(dp: Dispatcher):  # Register of oops_handler
    dp.register_message_handler(oops,)
