from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = KeyboardButton("отменить делегирование")
recipient_spec = KeyboardButton('SPEC')

cancel_delegated = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_delegated.add(recipient_spec).add(cancel)
