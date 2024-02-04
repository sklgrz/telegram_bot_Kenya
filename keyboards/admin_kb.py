from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/пусто1')
b2 = KeyboardButton('/пусто2')
b3 = KeyboardButton('/пусто3')
b4 = KeyboardButton('/пусто4')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b1).add(b2).row(b3, b4)
