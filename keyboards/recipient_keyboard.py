from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

recipient_for_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
recipient_for_head = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

head = KeyboardButton('HEAD')
spec = KeyboardButton('SPEC')

recipient_for_admin.add(head, spec)
recipient_for_head.add(spec)
