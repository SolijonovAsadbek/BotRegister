from aiogram import Router, F
from aiogram.types import Message
from telegraph import Telegraph

from keyboards.inline.button import btn_tests

study_router = Router()
tg = Telegraph()


@study_router.message(F.text == '📚 Darsliklar')
async def educational(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>📚 Darsliklar</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">📚 Darsliklar</a>")


@study_router.message(F.text == '👨‍🏫 Kurslar')
async def educational(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>👨‍🏫 Kurslarimiz</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Kurslar</a>")


@study_router.message(F.text == '🧑‍💻 Testlar')
async def educational(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>🧑‍💻 Testlar</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Kurslar</a>", reply_markup=btn_tests())


@study_router.message(F.text == '📊 Statistika')
async def educational(message: Message):
    tg.create_account(short_name='1337')

    response = tg.create_page(
        'Assalomu alaykum!',
        html_content='<p>📊 Statistika</p>'
    )
    await message.answer(text=f"<a href=\"{response['url']}\">👨‍🏫 Kurslar</a>")
