import json

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.db.db_sqlalch import BASE_DIR

quiz_router = Router()


async def load_quizs(category):
    with open(f'{BASE_DIR}/handlers/savollar.json') as savollar:
        quizs = json.load(savollar)
        quizs = [quiz for quiz in quizs if quiz['category'] == category]
    return quizs


@quiz_router.callback_query(lambda call: call.data in ['math', 'physics', 'english'])
async def start_quiz(call: CallbackQuery, state: FSMContext):
    quizs = await load_quizs(call.data)
    await state.update_data(index=0, score=0)
    index = await state.get_value('index')
    # score = await state.get_value('score')
    #
    quiz = quizs[index]['question']['uz']
    options = quizs[index]['options']

    builder = InlineKeyboardBuilder()
    for text in options:
        builder.button(text=text, callback_data=f"opt_{text.lower()}")
    builder.adjust(2, 2)

    await call.message.answer(f"{quiz}", reply_markup=builder.as_markup())


@quiz_router.callback_query(lambda call: call.data.startswith('opt_'))
async def get_answer(call: CallbackQuery, state: FSMContext):
    quizs = await load_quizs(call.data)
    index = await state.get_value('index')


if __name__ == '__main__':
    print(BASE_DIR)
