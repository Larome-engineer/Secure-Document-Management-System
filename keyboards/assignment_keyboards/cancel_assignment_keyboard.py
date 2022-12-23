from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_creating = KeyboardButton("Oтменить создание")

cancel_a = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_a.add(cancel_creating)
