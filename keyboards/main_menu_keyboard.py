from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

documents = KeyboardButton("Документы")
assignments = KeyboardButton("Поручения")
logout = KeyboardButton("Выйти")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(documents).add(assignments).add(logout)
