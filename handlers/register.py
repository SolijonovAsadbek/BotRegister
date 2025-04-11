from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert, select, update
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.button import share_contact
from utils.db.db_sqlalch import user, engine, save_language_to_database

from states.register import RegisterState

register_router = Router()


@register_router.callback_query(lambda call: call.data in ['uz', 'ru', 'en'])
async def change_language(call: CallbackQuery):
    # await call.message.delete()
    til = call.data
    chat_id = call.message.chat.id
    await save_language_to_database(chat_id, til)
    await call.message.edit_text(f"<b>{til}</b> tiliga o'zgardi!")
    # await call.message.answer(f"<b>{til}</b> tiliga o'zgardi!")


@register_router.callback_query(RegisterState.lang)
async def save_lang(call: CallbackQuery, state: FSMContext):
    til = call.data  # uz, ru, en
    chat_id = call.message.chat.id  # 214892189

    await save_language_to_database(chat_id, til)

    await state.set_state(RegisterState.fullname)
    await call.message.answer("Til qo'shildi", reply_markup=ReplyKeyboardRemove())
    await call.message.answer("To'liq ismingiz kiriting: ")


@register_router.message(RegisterState.fullname)
async def save_fullname(message: Message, state: FSMContext):
    fullname = message.text
    chat_id = message.chat.id

    with engine.connect() as conn:
        query = update(user).where(user.c.chat_id == chat_id).values(fullname=fullname)
        conn.execute(query)
        conn.commit()

    await state.set_state(RegisterState.phone)
    await message.answer("Ism qo'shildi")
    await message.answer("Telefon raqamingizni kiriting yoki ulashing: ", reply_markup=share_contact())


@register_router.message(F.text == '📲 Raqamni ulashish')
@register_router.message(RegisterState.phone)
async def save_fullname(message: Message, state: FSMContext):
    chat_id = message.chat.id
    phone = message.text

    if message.contact:
        phone = message.contact.phone_number

    with engine.connect() as conn:
        query = update(user).where(user.c.chat_id == chat_id).values(phone=phone)
        conn.execute(query)
        conn.commit()

    await state.set_state(RegisterState.fullname)
    await message.answer("Telefon raqam qo'shildi", reply_markup=ReplyKeyboardRemove())
    await state.clear()
