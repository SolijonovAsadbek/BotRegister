from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def study_menu():
    darslik = KeyboardButton(text='📚 Darsliklar')
    kurslar = KeyboardButton(text='👨‍🏫 Kurslar')
    test = KeyboardButton(text='🧑‍💻 Testlar')
    statistika = KeyboardButton(text='📊 Statistika')
    til_uzgartirish = KeyboardButton(text="🌐 Tilni o'zgartirish")

    btns = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [darslik, kurslar],
        [test, statistika],
        [til_uzgartirish]
    ])

    return btns


def share_contact():
    contact = KeyboardButton(text='📲 Raqamni ulashish', request_contact=True)

    btn = ReplyKeyboardMarkup(keyboard=[
        [contact]
    ])

    return btn
