import os
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, MetaData, Table,
                        Column, Integer, String, select, insert, update, DateTime, func, Boolean, ForeignKey,
                        UniqueConstraint)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASE_URL = os.path.join(f'sqlite:///{BASE_DIR}', 'sqlite.db')
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()
meta = MetaData()


#
user = Table('user', meta,
             Column('chat_id', Integer, primary_key=True),
             Column('fullname', String),
             Column('username', String),
             Column('phone', String),
             Column('lang', String))


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'), nullable=False)
    text = Column(String(500), nullable=False)
    explanation = Column(String(500), nullable=True)
    difficulty = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    fullname = Column(String)
    username = Column(String)
    phone = Column(String)
    lang = Column(String)
    created_at = Column(DateTime, default=func.now())


class UserAnswer(Base):
    __tablename__ = 'user_answer'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    option_id = Column(Integer, ForeignKey('option.id'), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'quiz_id', name='_user_quiz_uc'),
    )


if __name__ == '__main__':
    meta.create_all(engine)

    # with engine.connect() as conn:
    #     query = insert(user).values(chat_id=2341,
    #                                 fullname='goerge',
    #                                 username='mathcareerpy',
    #                                 phone='949023212',
    #                                 lang='ru')
    #     conn.execute(query)
    #     conn.commit()
    #
    # # SELECT bilan natijalarni olish
    # query = select(user)
    # datas = conn.execute(query).fetchall()
    # print(datas)
    #
    # # WHERE bilan ma'lumot qidirish
    # query = select(user).where(user.c.chat_id == 6490355760)
    # data = conn.execute(query).fetchone()
    # print(data)
    #
    # # LIKE bilan ma'lumot qidirish
    # query = select(user).where(user.c.fullname.like('A%'))
    # data = conn.execute(query).fetchall()
    # print(data)
    Base.metadata.create_all(bind=engine)
