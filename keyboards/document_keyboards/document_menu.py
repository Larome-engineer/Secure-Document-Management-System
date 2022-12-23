from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

all_docx = KeyboardButton("Все документы")
upload = KeyboardButton("Загрузить документ")
sign_doc = KeyboardButton("Подписать документ")
revision = KeyboardButton("Отправить на доработку")
remove = KeyboardButton("Удалить документ")
back = KeyboardButton("Назад")
logout = KeyboardButton("Выйти")

doc_menu = ReplyKeyboardMarkup(resize_keyboard=True)
doc_menu.add(all_docx).add(upload).add(sign_doc).add(revision).add(remove).add(back).add(logout)
