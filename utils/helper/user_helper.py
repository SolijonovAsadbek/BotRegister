import asyncio

from sqlalchemy import select, insert, update

from utils.db.db_sqlalchemy import engine, User, Category, SubCategory, Quiz, Option


async def check_registration(chat_id):
    with engine.connect() as conn:
        query = select(User).where(User.chat_id == chat_id)
        result = conn.execute(query).fetchone()
        return bool(result)  # True/False


async def register(**kwargs):
    with engine.connect() as conn:
        query = insert(User).values(**kwargs)
        conn.execute(query)
        conn.commit()


async def save_language_to_database(chat_id, til):
    with engine.connect() as conn:
        query = update(User).where(User.chat_id == chat_id).values(lang=til)
        conn.execute(query)
        conn.commit()


async def followers_count():
    with engine.connect() as conn:
        query = select(User)
        users_count = len(conn.execute(query).fetchall())
    return users_count


def get_categories():
    with engine.connect() as conn:
        query = select(Category.id, Category.name)
        datas = conn.execute(query).fetchall()
    return datas


def get_subcategories(cat_id):
    with engine.connect() as conn:
        query = select(SubCategory.id, SubCategory.name).where(SubCategory.category_id == cat_id)
        datas = conn.execute(query).fetchall()
    return datas


def get_quizzes(sub_id):
    with engine.connect() as conn:
        query = select(Quiz.id, Quiz.text).where(Quiz.subcategory_id == sub_id)
        datas = conn.execute(query).fetchall()
    return datas


def get_options(quiz_id):
    with engine.connect() as conn:
        query = select(Option.text, Option.is_correct).where(Option.quiz_id == quiz_id)
        datas = conn.execute(query).fetchall()
    return datas


if __name__ == '__main__':
    categories = asyncio.run(get_categories())
    print(categories)
    for cat_id, cat_name in categories:
        print(cat_name)
        subcateories = asyncio.run(get_subcategories(cat_id))
        for sub_id, sub_name in subcateories:
            print(sub_name)
            quizzes = asyncio.run(get_quizzes(sub_id))
            for q_id, q_text in quizzes:
                print(q_text)
                options = asyncio.run(get_options(q_id))
                for option, is_correct in options:
                    print(f"{option:.<30}{is_correct}")
