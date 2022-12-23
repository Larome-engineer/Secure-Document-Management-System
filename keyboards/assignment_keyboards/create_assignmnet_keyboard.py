from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

recipient_head = KeyboardButton('HEAD')
recipient_spec = KeyboardButton('SPEC')
cancel_creating = KeyboardButton("Oтменить создание")

select_recipient_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
select_recipient_head = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

select_recipient_admin.add(recipient_head).add(recipient_spec).add(cancel_creating)
select_recipient_head.add(recipient_spec).add(cancel_creating)
