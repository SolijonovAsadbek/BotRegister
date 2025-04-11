from aiogram.fsm.state import StatesGroup, State


class QuizState(StatesGroup):
    quession = State()
    score = State()
