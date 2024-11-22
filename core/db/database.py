from datetime import datetime
from typing import List
from core.config import DB_USER, DB_HOST, DB_NAME, DB_PASS, DB_PORT

from sqlalchemy import text, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=False)
session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class CandidatesDB(Base):
    __tablename__ = 'candidates'

    first_name = mapped_column(String(20), nullable=False)
    second_name = mapped_column(String(20), nullable=False)
    age: Mapped[int]
    status: Mapped[int]
    city = mapped_column(String(20), nullable=False)
    desired_position = mapped_column(String(30), index=True, nullable=False)
    education_degree: Mapped[int]
    working_experience = mapped_column(String(1000))
    about_oneself = mapped_column(String(1000))
    published: Mapped[bool] = mapped_column(default=True)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now()) "))

    skills: Mapped[List["CandidatesSkillsDB"]] = relationship()


class CandidatesSkillsDB(Base):
    __tablename__ = 'candidates_skills'

    foreign_key: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    skill_name = mapped_column(String(30), nullable=False)
    indexing_skill_name = mapped_column(String(30), index=True, nullable=False)
    level: Mapped[int]
    years_of_experience: Mapped[int]
    last_used_year: Mapped[int]
    score: Mapped[int]


class JobOpeningsDB(Base):
    __tablename__ = 'job_openings'

    title = mapped_column(String(40), index=True, nullable=False)
    description = mapped_column(String(1000))
    address = mapped_column(String(100), index=True, nullable=False)
    salary: Mapped[int] = mapped_column(index=True)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now()) "))

    skills: Mapped[List["RequiredSkillsDB"]] = relationship()
    skills_quantity: Mapped[int]


class RequiredSkillsDB(Base):
    __tablename__ = 'required_skills'

    foreign_key: Mapped[int] = mapped_column(ForeignKey("job_openings.id", ondelete="CASCADE"), index=True)
    skill_name = mapped_column(String(30), nullable=False)
    indexing_skill_name = mapped_column(String(30), index=True, nullable=False)
    level: Mapped[int]
    years_of_experience: Mapped[int]
    score: Mapped[int]
