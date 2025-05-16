import os
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, func

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "1234"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5436"
POSTGRES_DB = "ziyo_test_db"

# Connection URLs
SYNC_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create engines
sync_engine = create_engine(SYNC_DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model
Base = declarative_base()
session = SessionLocal()


# Synchronous session usage example
def get_db():
    """Synchronous session generator for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Asynchronous session usage example
async def get_async_db():
    """Asynchronous session generator for dependency injection"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    subcategories = relationship('SubCategory',
                                 cascade="all, delete-orphan",
                                 back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name!r})>"


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer,
                         ForeignKey('category.id', ondelete="CASCADE"),
                         nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    category = relationship('Category', back_populates='subcategories')
    quizzes = relationship('Quiz',
                           cascade="all, delete-orphan",
                           back_populates='subcategory')

    def __repr__(self):
        return f"<SubCategory(id={self.id}, name={self.name!r})>"


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer,
                            ForeignKey('subcategory.id', ondelete="CASCADE"),
                            nullable=False)
    text = Column(String(500), nullable=False)
    explanation = Column(String(500), nullable=True)
    difficulty = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())

    # Relationships
    subcategory = relationship('SubCategory', back_populates='quizzes')
    options = relationship('Option',
                           cascade="all, delete-orphan",
                           back_populates='quiz')
    user_answers = relationship('UserAnswer',
                                cascade="all, delete-orphan",
                                back_populates='quiz')

    def __repr__(self):
        return f"<Quiz(id={self.id}, text={self.text[:20]}...)>"


class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer,
                     ForeignKey('quiz.id', ondelete="CASCADE"),
                     nullable=False)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz = relationship('Quiz', back_populates='options')
    user_answers = relationship('UserAnswer',
                                cascade="all, delete-orphan",
                                back_populates='option')

    def __repr__(self):
        return f"<Option(id={self.id}, text={self.text[:20]}..., correct={self.is_correct})>"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    fullname = Column(String)
    username = Column(String, unique=True)
    phone = Column(String)
    lang = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    answers = relationship('UserAnswer',
                           cascade="all, delete-orphan",
                           back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username!r})>"


class UserAnswer(Base):
    __tablename__ = 'user_answer'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete="CASCADE"),
                     nullable=False)
    quiz_id = Column(Integer,
                     ForeignKey('quiz.id', ondelete="CASCADE"),
                     nullable=False)
    option_id = Column(Integer,
                       ForeignKey('option.id', ondelete="CASCADE"),
                       nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship('User', back_populates='answers')
    quiz = relationship('Quiz', back_populates='user_answers')
    option = relationship('Option', back_populates='user_answers')

    def __repr__(self):
        return f"<UserAnswer(user_id={self.user_id}, quiz_id={self.quiz_id}, option_id={self.option_id})>"


def show_quizs():
    # Create a new session
    session = SessionLocal()

    try:
        categories = session.query(Category).all()
        for category in categories:
            print(category.name, end=' -> ')
            for subcategory in category.subcategories:
                print(f"{subcategory.name}")
                for quiz_index, quiz in enumerate(subcategory.quizzes, start=1):
                    print(f"    {quiz_index}-savol: {quiz.text}")
                    variants = ['a', 'b', 'c', 'd']
                    for abc, option in zip(variants, quiz.options):
                        print(f"        {abc}) {option.text:.<30}{f'{option.is_correct}'}")
    finally:
        session.close()


# Initialize database (synchronous version)
def init_db():
    Base.metadata.create_all(bind=sync_engine)


# Initialize database (asynchronous version)
async def async_init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    init_db()  # Synchronous
    print("Database tables created successfully!")
    show_quizs()
