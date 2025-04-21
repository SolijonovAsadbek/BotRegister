import json
import os

from aiogram import Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from random import sample, shuffle

from handlers.menu import educational_test
from keyboards.inline.button import keyboard_builder, btn_confirm, btn_one_confirm
from states import QuizState
from utils.db.db_sqlalchemy import BASE_DIR
from utils.helper.user_helper import get_categories

quiz_router = Router()


async def load_quizs(category):
    file_path = f'{BASE_DIR}/utils/db/savollar.json'

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path) as savollar:
            quizs = json.load(savollar)
        quizs = [quiz for quiz in quizs if quiz['category'] == category]
        return quizs if quizs else None
    except json.decoder.JSONDecodeError:
        return None


async def build_keyboard(options):
    options = [(text, text) for text in options]
    adjust = (2,)
    keyboards = keyboard_builder(options, adjust)
    return keyboards


async def send_question(call: CallbackQuery, state: FSMContext, index: int, score: int, quizs: list):
    quiz_number = index + 1

    if index >= len(quizs):
        test = await state.get_value('quizs')
        await state.clear()
        await call.message.edit_text(f"Sizning {test[0]['category']} natijangiz {score} ball")
        return

    quiz_text = quizs[index]['question']['uz']
    options = quizs[index]['options']
    shuffle(options)

    quiz_keyboard = await build_keyboard(options)

    await call.message.edit_text(html.bold(f"{quiz_number}-savol: {quiz_text}"), reply_markup=quiz_keyboard)
    await state.set_state(QuizState.quession)


@quiz_router.callback_query(lambda call: call.data in [d for d, c in get_categories()])
async def start_quiz(call: CallbackQuery, state: FSMContext):
    if quizs := await load_quizs(call.data):
        await state.set_state(QuizState.confirm)
        await state.update_data(quizs=quizs)
        await call.message.edit_text(f'{call.data} savollarni boshlashga tayyormisiz!', reply_markup=btn_confirm)
    else:
        await state.set_state(QuizState.confirm)
        await call.message.edit_text(f'{call.data} savollar mavjud emas!', reply_markup=btn_one_confirm)


@quiz_router.callback_query(QuizState.quession)
async def get_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quizs = data.get('quizs')
    index = data.get('index', 0)
    score = data.get('score', 0)
    answer = quizs[index]['answer']

    if answer == call.data:
        score += 1
        await call.answer(f'+1 | Ball: {score}')
    else:
        await call.answer(f'Xato!')
    index += 1
    await state.update_data(index=index, score=score)
    await send_question(call, state, index, score, quizs)


@quiz_router.callback_query(QuizState.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        quizs = await state.get_value('quizs')
        quizs = sample(quizs, min(len(quizs), 5))
        await state.update_data(quizs=quizs)
        await send_question(call, state, 0, 0, quizs)
    else:
        await state.clear()
        await educational_test(call)
