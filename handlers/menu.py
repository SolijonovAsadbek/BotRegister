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


# @menu_router.message(F.text == '📊 Statistika')
# async def send_statistics_image(message: types.Message):
#     try:
#         results = show_statistics() * 10
#         img = generate_stats_image(results)
#         photo = BufferedInputFile(img.read(), filename="statistika.png")
#         await message.answer_photo(photo=photo, caption="📊 Testlar statistikasi")
#     except Exception as e:
#         await message.answer(f"Statistika yaratishda xato: {str(e)}")


def truncate_text(draw, text, max_width, font):
    """Matnni max_width ga sig‘adigancha kesib beradi"""
    ellipsis = "..."
    while draw.textlength(text, font=font) > max_width:
        if len(text) <= 1:
            return ellipsis
        text = text[:-1]
    return text


def generate_stats_image(results):
    # Fontlarni o'rnatish
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # O'lchamlar
    line_height = 30
    padding = 40
    width = 800
    col_widths = [50, 300, 100, 100, 100]  # Ustunlar: #, Ism, To'g'ri, Jami, Foiz
    height = padding * 2 + len(results) * line_height + 100

    # Rasm yaratish
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Sarlavha
    draw.text((padding, padding), "📊 Testlar statistikasi", fill='black', font=font_large)

    # Jadval sarlavhalari
    headers = ["№", "Ism", "To'g'ri", "Jami", "Foiz"]
    header_y = padding + 50

    for i, (text, col_w) in enumerate(zip(headers, col_widths)):
        x = padding + sum(col_widths[:i])
        draw.rectangle([x, header_y, x + col_w, header_y + line_height], outline='gray')
        draw.text((x + 5, header_y + 5), text, fill='black', font=font_medium)

    # Ma'lumotlar
    for row_num, (fullname, correct, total, percent) in enumerate(results, start=1):
        row_y = header_y + line_height + (row_num - 1) * line_height

        data = [
            str(row_num),
            truncate_text(draw, fullname, col_widths[1] - 10, font_small),
            str(correct),
            str(total),
            f"{percent}%",
        ]

        for i, (text, col_w) in enumerate(zip(data, col_widths)):
            x = padding + sum(col_widths[:i])
            draw.rectangle([x, row_y, x + col_w, row_y + line_height], outline='gray')
            draw.text((x + 5, row_y + 5), text, fill='black', font=font_small)

    # Rasmni xotiraga yozish
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


@menu_router.message(F.text == "🌐 Tilni o'zgartirish")
async def again_choose_language(message: Message):
    await choose_language(message)
