from sqlalchemy import select, update, insert, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .models import TopUp, UsageHistory
import os

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, future=True)

async_session: AsyncSession = sessionmaker(engine, class_=AsyncSession)

async def add_credits_to_telegram_user(session, telegram_user_id: str, amount: int, created_at):
    stm = insert(TopUp).values(
        telegram_user_id=telegram_user_id,
        amount=amount,
        created_at=created_at,
    )
    await session.execute(stm)


async def get_user_usage_history(session, telegram_user_id: str):
    result = await session.scalars(
        select(UsageHistory).where(UsageHistory.telegram_user_id == telegram_user_id)
    )
    return result.all()


async def get_user_topups(session, telegram_user_id: str):
    result = await session.scalars(
        select(TopUp).where(TopUp.telegram_user_id == telegram_user_id)
    )
    return result.all()


async def insert_usage(session, telegram_user_id, predict_time, prediction_id, created_at):
    stm = insert(UsageHistory).values(
         telegram_user_id=telegram_user_id,
         predict_time=predict_time,
         prediction_id=prediction_id,
         created_at=created_at
    )
    await session.execute(stm)
