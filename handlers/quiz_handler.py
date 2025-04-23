from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from typing import Union

from handlers.callback_data import NavigationCallback
from keyboards.inline.button import navigation_keyboard
from utils.helper.user_helper import get_categories_async, get_subcategories, get_quizzes, get_options

quiz_handler = Router()


@quiz_handler.message(F.text == '🧑‍💻 Testlar')
async def show_categories(message: Message):
    categories = await get_categories_async()
    kb_categories = navigation_keyboard(categories, 'category')
    await message.answer("🧑‍💻 Testlar bo‘limi:", reply_markup=kb_categories)


@quiz_handler.callback_query(NavigationCallback.filter())
async def handle_navigation(call: CallbackQuery, callback_data: NavigationCallback):
    data = callback_data
    level = data.level

    text = ""
    items = []
    keyboard = None

    # Har bir darajaga mos ravishda kerakli ma'lumotlarni olish
    if level == "category":
        items = await get_subcategories(data.category_id)
        text = "🗂 Subkategoriyani tanlang:"
        keyboard = navigation_keyboard(items, level="subcategory", category_id=data.category_id)

    elif level == "subcategory":
        items = await get_quizzes(data.subcategory_id)
        text = "📝 Quizni tanlang:"
        keyboard = navigation_keyboard(items, level="quiz", category_id=data.category_id, subcategory_id=data.subcategory_id)

    elif level == "quiz":
        items = await get_options(data.quiz_id)
        text = "✅ Variantni tanlang:"
        keyboard = navigation_keyboard(items, level="option", category_id=data.category_id, subcategory_id=data.subcategory_id, quiz_id=data.quiz_id)

    elif level == "option":
        await call.answer("✅ Variant tanlandi!", show_alert=True)
        return

    # Hozirgi matn va reply_markupni solishtirish
    current_text = call.message.text
    current_markup = call.message.reply_markup

    # Matnni va markupni faqat kerakli holatda yangilash
    if current_text != text or current_markup != keyboard:
        try:
            # Matn va markupni yangilash
            await call.message.edit_text(text=text, reply_markup=keyboard)
        except Exception as e:
            await call.answer("⚠️ Xatolik yuz berdi.")
            print("Edit text error:", e)
    else:
        await call.answer("⏪ Oldingi holatda turibsiz.")


