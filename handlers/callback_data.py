from aiogram.filters.callback_data import CallbackData


# class TestCase
class NavigationCallback(CallbackData, prefix="nav"):
    level: str  # 'category', 'subcategory', 'quiz', 'option'
    category_id: int = 0
    subcategory_id: int = 0
    quiz_id: int = 0
