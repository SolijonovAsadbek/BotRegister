import asyncio
from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.callback_data import NavigationCallback


def keyboard_builder(keyboards: List, adjust: tuple):
    builder = InlineKeyboardBuilder()
    for id, text in keyboards:
        builder.button(text=text, callback_data=str(id))

    builder.adjust(*adjust)
    keyboards = builder.as_markup()
    return keyboards


keyboards_lang = [("🇺🇿 Uzbek", "uz"), ("🇷🇺 Russian", "ru"), ("🇺🇸 English", "en")]
keyboards_confirm = [("✅ Ha", "yes"), ("⬅️ Ortga", "back")]
keyboards_one_confirm = [("⬅️ Ortga", "back")]

btn_langs = keyboard_builder(keyboards_lang, (3,))
btn_confirm = keyboard_builder(keyboards_confirm, (2,))
btn_one_confirm = keyboard_builder(keyboards_one_confirm, (1,))


def navigation_keyboard(items: list[tuple[str, int]], level: str, **ids):
    builder = InlineKeyboardBuilder()

    for title, item_id in items:
        cb_data = NavigationCallback(level=level, **ids, **{
            f"{level}_id": item_id
        }).pack()
        builder.button(text=title, callback_data=cb_data)

    # Ortga tugmasi
    if level != "category":
        back_level = {
            "subcategory": "category",
            "quiz": "subcategory",
            "option": "quiz"
        }[level]

        # Orqaga tugmasini har doim yangi callback_data bilan yaratish
        cb_back = NavigationCallback(level=back_level, **ids).pack()

        # Orqaga tugmasi bo'lsa, uni yaratish
        builder.button(text="⬅️ Ortga", callback_data=cb_back)

    builder.adjust(2)
    return builder.as_markup()

