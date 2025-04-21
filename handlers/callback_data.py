from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix='cat'):
    id: int


class SubCategoryCallback(CallbackData, prefix='sub'):
    id: int
    cat: int


class QuizCallback(CallbackData, prefix='quiz'):
    id: int
    sub: int


class OptionCallback(CallbackData, prefix='option'):
    id: int
    quiz: int


class BackCallback(CallbackData, prefix='back'):
    level: int
    paylod: int
