import io

from aiogram import Router, F, types
from aiogram.types import Message, BufferedInputFile
from telegraph import Telegraph
from PIL import Image, ImageDraw, ImageFont

from handlers.start import choose_language
from utils.helper.user_helper import show_statistics

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
    results = show_statistics()

    html_content = ("<p><b>📊 Umumiy statistika natijalari</b></p>"
                    "<p><b>Quyidagi jadvalda foydalanuvchilarning testdagi ishtiroki ko'rsatilgan:</b></p>")

    for index, (fullname, correct, total, percent) in enumerate(results, start=1):
        html_content += (
            f"<p style='border:1px solid #ccc; padding:10px; margin:10px 0;'>"
            f"<b>👤 {index} {fullname}</b>"
            f"<b> - {percent}%</b><br>"
            f"✅ To'g'ri javoblar: <b>{correct}</b><br>"
            f"📋 Jami javoblar: <b>{total}</b>"
            f"</p>"
        )

    response = tg.create_page(
        title="Statistika",
        html_content=html_content
    )

    await message.answer(
        text=f"<a href=\"{response['url']}\">👨‍🏫 Statistika</a>",
        parse_mode="HTML"
    )


@menu_router.message(F.text == "🌐 Tilni o'zgartirish")
async def again_choose_language(message: Message):
    await choose_language(message)
