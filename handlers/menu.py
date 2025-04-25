from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegraph import Telegraph

from handlers.start import choose_language

menu_router = Router()
tg = Telegraph()


@menu_router.message(F.text == '📚 Darsliklar')
async def educational_lesson(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>📚 Darsliklar</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">📚 Darsliklar</a>")


@menu_router.message(F.text == '👨‍🏫 Kurslar')
async def educational_course(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>👨‍🏫 Kurslarimiz</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Kurslar</a>")


@menu_router.message(F.text == '📊 Statistika')
async def educational_statistics(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>📊 Statistika</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Statistika</a>")


@menu_router.message(F.text == "🌐 Tilni o'zgartirish")
async def again_choose_language(message: Message):
    await choose_language(message)
