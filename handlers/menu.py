from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegraph import Telegraph

from handlers.start import choose_language
from keyboards.inline.button import keyboard_builder
from utils.helper.user_helper import get_categories

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


@menu_router.message(F.text == '🧑‍💻 Testlar')
async def educational_test(message: Union[Message, CallbackQuery]):
    tg.create_account(short_name='1337')
    test_categories = keyboard_builder(get_categories(), (2,))
    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>🧑‍💻 Testlar</p>'
    )
    if isinstance(message, Message):
        await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Testlar</a>", reply_markup=test_categories)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(text=f"<a href=\"{response['url']}\">👨‍🏫 Testlar</a>",
                                        reply_markup=test_categories)


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
