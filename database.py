from datetime import datetime
from typing import List
from config import DB_USER, DB_HOST, DB_NAME, DB_PASS, DB_PORT

from sqlalchemy import text, inspect, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class CandidatesDB(Base):
    __tablename__ = 'candidates'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = mapped_column(String(20), nullable=False)
    second_name = mapped_column(String(20), nullable=False)
    age: Mapped[int]
    status: Mapped[int]
    desired_position = mapped_column(String(30), index=True, nullable=False)
    education_degree: Mapped[int]
    working_experience = mapped_column(String(1000))
    about_oneself = mapped_column(String(1000))
    published: Mapped[bool] = mapped_column(default=True)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now()) "))

    skills: Mapped[List["SkillsDB"]] = relationship()


class SkillsDB(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))
    skill_name = mapped_column(String(30), index=True, nullable=False)
    years_of_experience: Mapped[int]
    last_used_year: Mapped[int]


async def create_table():
    """
    Create all tables.
    """
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

    if not (CandidatesDB.__tablename__ in tables and SkillsDB.__tablename__ in tables):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
