from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/Посоветоваться')
b2 = KeyboardButton('/Найти_текст_песни')
b3 = KeyboardButton('/Погода')
b4 = KeyboardButton('/Пароль')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).row(b3, b4)
