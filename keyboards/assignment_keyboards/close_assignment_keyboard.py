from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

close = KeyboardButton("Отменить закрытие")

cancel_close = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_close.add(close)
