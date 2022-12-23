from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

download = KeyboardButton("Отменить загрузку документа")
sign = KeyboardButton("Отменить подписание")
revision = KeyboardButton("Отменить доработку")
deleting = KeyboardButton("Отменить удаление")

k_cancel_downloading = ReplyKeyboardMarkup(resize_keyboard=True)
k_cancel_downloading.add(download)

k_cancel_signing = ReplyKeyboardMarkup(resize_keyboard=True)
k_cancel_signing.add(sign)

k_cancel_revision = ReplyKeyboardMarkup(resize_keyboard=True)
k_cancel_revision.add(revision)

k_cancel_deleting = ReplyKeyboardMarkup(resize_keyboard=True)
k_cancel_deleting.add(deleting)
