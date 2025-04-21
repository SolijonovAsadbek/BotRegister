import asyncio
from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.helper.user_helper import get_categories


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


def nested_keyboard_builder(data, cb_class, adjust, extra_data=None, back=None):
    kb = InlineKeyboardBuilder()
    for id, data in data:
        kwargs = {'id': id}
        if extra_data:
            kwargs.update(extra_data)
        callback = cb_class(**kwargs)
        kb.button(text=data, callback_data=callback.pack())
    kd.adjust()
