from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def btn_langs():
    uz = InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data='uz')
    ru = InlineKeyboardButton(text="🇷🇺 Russian", callback_data='ru')
    en = InlineKeyboardButton(text="🇺🇸 English", callback_data='en')

    btns = InlineKeyboardMarkup(inline_keyboard=[
        [uz, ru, en]
    ])
    return btns


def btn_tests():
    uz = InlineKeyboardButton(text="➕ Matematika", callback_data='math')
    ru = InlineKeyboardButton(text="♾️ Fizika", callback_data='physics')
    en = InlineKeyboardButton(text="🇺🇸 English", callback_data='english')

    btns = InlineKeyboardMarkup(inline_keyboard=[
        [uz, ru],
        [en, ]
    ])
    return btns
