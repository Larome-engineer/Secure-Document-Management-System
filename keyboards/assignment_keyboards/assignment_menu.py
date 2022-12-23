from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

all_assignments = KeyboardButton("Все поручения")
new_assignment = KeyboardButton("Новое поручение")
close_assignment = KeyboardButton("Закрыть поручение")
delegate_assignment = KeyboardButton("Делегировать поручение")
back = KeyboardButton("Назад")
logout = KeyboardButton("Выйти")

a_menu = ReplyKeyboardMarkup(resize_keyboard=True)
a_menu.add(all_assignments).add(new_assignment).add(close_assignment).add(delegate_assignment).add(back).add(logout)
