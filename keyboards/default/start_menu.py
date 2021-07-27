from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_start():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('😎Наличие товаров', '📥Помощь')
    markup.add('🔄Замена', '📖Правила')
    markup.add('💰Пополнить баланс', '😎Профиль')
    markup.add('👤Реферальная система')
    return markup


def reset_payment_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💰Отмена')
    return markup
