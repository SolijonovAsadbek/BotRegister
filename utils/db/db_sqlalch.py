import os
from sqlalchemy import (create_engine, MetaData, Table,
                        Column, Integer, String, select, insert, update)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASE_URL = os.path.join(f'sqlite:///{BASE_DIR}', 'sqlite.db')

engine = create_engine(DATABASE_URL, echo=False)

meta = MetaData()

user = Table('user', meta,
             Column('chat_id', Integer, primary_key=True),
             Column('fullname', String),
             Column('username', String),
             Column('phone', String),
             Column('lang', String))

meta.create_all(engine)


async def check_registration(chat_id):
    with engine.connect() as conn:
        query = select(user).where(user.c.chat_id == chat_id)
        result = conn.execute(query).fetchone()
        return bool(result)  # True/False


async def register(**kwargs):
    with engine.connect() as conn:
        query = insert(user).values(**kwargs)
        conn.execute(query)
        conn.commit()


async def save_language_to_database(chat_id, til):
    with engine.connect() as conn:
        query = update(user).where(user.c.chat_id == chat_id).values(lang=til)
        conn.execute(query)
        conn.commit()


if __name__ == '__main__':
    with engine.connect() as conn:
        query = insert(user).values(chat_id=2341,
                                    fullname='goerge',
                                    username='mathcareerpy',
                                    phone='949023212',
                                    lang='ru')
        conn.execute(query)
        conn.commit()

    # SELECT bilan natijalarni olish
    query = select(user)
    datas = conn.execute(query).fetchall()
    print(datas)

    # WHERE bilan ma'lumot qidirish
    query = select(user).where(user.c.chat_id == 6490355760)
    data = conn.execute(query).fetchone()
    print(data)

    # LIKE bilan ma'lumot qidirish
    query = select(user).where(user.c.fullname.like('A%'))
    data = conn.execute(query).fetchall()
    print(data)
