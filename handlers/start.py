import sqlalchemy
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import html, Router, F
from sqlalchemy import insert

from keyboards.default.button import study_menu
from keyboards.inline.button import btn_langs
from utils.db.db_sqlalch import user, engine, check_registration, register
from states.register import RegisterState

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    await message.answer(f"Assalomu alaykum, {html.bold(message.from_user.full_name)}!",
                         reply_markup=ReplyKeyboardRemove())

    if await check_registration(chat_id):
        # Boshqa menyuga o'tkazish
        await message.answer('Quyidagi tugmalardan birini tanlang!', reply_markup=study_menu())
    else:
        try:
            # Ma'lumotlar ba'zasiga default yozish
            await register(chat_id=chat_id, fullname=fullname, username=username)
        except sqlalchemy.exc.IntegrityError as e:
            await message.answer(f"Error: {e}")
        else:
            # Tilni tanlash uchun
            await choose_language(message)
            # state o'tkazish
            await state.set_state(RegisterState.lang)


@start_router.message(F.text == "🌐 Tilni o'zgartirish")
async def again_choose_language(message: Message):
    await choose_language(message)


async def choose_language(message):
    text = (f"O'zingizga mos til tanlang:\n"
            f"Выберите язык, подходящий для себя:\n"
            f"Choose a language suitable for yourself: \n")

    await message.answer(text, reply_markup=btn_langs())
