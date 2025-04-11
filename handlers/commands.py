from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from sqlalchemy import select
from utils.db.db_sqlalch import user, engine

command_router = Router()


@command_router.message(Command('obunachilar'))
async def followers_count(message: Message):
    with engine.connect() as conn:
        query = select(user)
        users_count = len(conn.execute(query).fetchall())
    await message.answer(f'Obunachilar soni {users_count} ta.')
