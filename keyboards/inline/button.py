from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard_builder(keyboards: List, adjust: tuple):
    builder = InlineKeyboardBuilder()
    for text, data in keyboards:
        builder.button(text=text, callback_data=data)

    builder.adjust(*adjust)
    keyboards = builder.as_markup()
    return keyboards


keyboards_lang = [("🇺🇿 Uzbek", "uz"), ("🇷🇺 Russian", "ru"), ("🇺🇸 English", "en")]
keyboards_test = [("➕ Matematika", "➕ Matematika"), ("♾️ Fizika", "♾️ Fizika"), ("🇺🇸 English", "🇺🇸 English"),
                  ("📜 Tarix", "📜 Tarix")]
keyboards_confirm = [("✅ Ha", "yes"), ("⬅️ Ortga", "back")]
keyboards_one_confirm = [("⬅️ Ortga", "back")]

btn_langs = keyboard_builder(keyboards_lang, (3,))
btn_tests = keyboard_builder(keyboards_test, (2,))
btn_confirm = keyboard_builder(keyboards_confirm, (2,))
btn_one_confirm = keyboard_builder(keyboards_one_confirm, (1,))
