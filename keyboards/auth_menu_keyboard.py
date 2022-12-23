from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

auth = KeyboardButton('Авторизация')
reg = KeyboardButton('Регистрация')
logout = KeyboardButton('Выйти')

auth_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
auth_keyboard.add(auth).add(reg).add(logout)
