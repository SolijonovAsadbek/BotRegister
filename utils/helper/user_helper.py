from sqlalchemy import select, insert, update

from utils.db.db_sqlalchemy import engine, User


async def check_registration(chat_id):
    with engine.connect() as conn:
        query = select(User).where(User.c.chat_id == int(chat_id))
        result = conn.execute(query).fetchone()
        return bool(result)  # True/False


async def register(**kwargs):
    with engine.connect() as conn:
        query = insert(User).values(**kwargs)
        conn.execute(query)
        conn.commit()


async def save_language_to_database(chat_id, til):
    with engine.connect() as conn:
        query = update(User).where(User.c.chat_id == int(chat_id)).values(lang=til)
        conn.execute(query)
        conn.commit()


async def followers_count():
    with engine.connect() as conn:
        query = select(User)
        users_count = len(conn.execute(query).fetchall())
    return users_count
