from sqlalchemy import inspect

from core.db.database import engine, CandidatesDB, JobOpeningsDB, RequiredSkillsDB, CandidatesSkillsDB, Base
from core.db.request_db import add_model_db
from core.schemas import AddCandidates, AddJobOpenings, AddRequiredSkills, AddCandidateSkills

candidates = [
    AddCandidates(
        first_name="Ilya", second_name="Safronov", age=28, status=2, city="Minsk", desired_position="Developer",
        education_degree=8, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="Python", level=2, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Php", level=0, years_of_experience=1, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Git", level=1, years_of_experience=1, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Docker", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=1, years_of_experience=2, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Masha", second_name="Asipova", age=18, status=2, city="Brest", desired_position="Developer",
        education_degree=8, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="Ruby", level=1, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Postgresql", level=0, years_of_experience=2, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="MachineLearning", level=1, years_of_experience=1, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Docker", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="Java", level=1, years_of_experience=2, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Danya", second_name="Mironov", age=22, status=3, city="Vitebsk", desired_position="Developer",
        education_degree=4, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="Python", level=0, years_of_experience=1, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Php", level=2, years_of_experience=7, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Java", level=1, years_of_experience=4, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Docker", level=0, years_of_experience=1, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=2, years_of_experience=4, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Dasha", second_name="Ageenko", age=25, status=1, city="Minsk", desired_position="Developer",
        education_degree=8, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="JavaScript", level=2, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="C++", level=1, years_of_experience=3, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="C", level=0, years_of_experience=1, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Spring", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=1, years_of_experience=2, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Pasha", second_name="Hatskevich", age=22, status=4, city="Borisow", desired_position="Developer",
        education_degree=3, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="Python", level=2, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Django", level=1, years_of_experience=2, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="FastAPI", level=1, years_of_experience=1, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Flask", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=1, years_of_experience=2, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Andrew", second_name="Mironenko", age=35, status=2, city="Minsk", desired_position="Developer",
        education_degree=8, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="JavaScript", level=2, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Node.js", level=1, years_of_experience=2, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Git", level=2, years_of_experience=10, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Docker", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=2, years_of_experience=10, last_used_year=2023
            )
        ]
    ),
    AddCandidates(
        first_name="Egor", second_name="Ermolovich", age=19, status=2, city="Minsk", desired_position="Game Developer",
        education_degree=8, working_experience="blablabla", about_oneself="blablabla", published=True, skills=[
            AddCandidateSkills(
                skill_name="C++", level=2, years_of_experience=4, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Php", level=0, years_of_experience=1, last_used_year=2024
            ),
            AddCandidateSkills(
                skill_name="Git", level=1, years_of_experience=1, last_used_year=2021
            ),
            AddCandidateSkills(
                skill_name="Docker", level=2, years_of_experience=5, last_used_year=2020
            ),
            AddCandidateSkills(
                skill_name="SQL", level=1, years_of_experience=2, last_used_year=2023
            )
        ]
    )
    ]


job_openings = [
    AddJobOpenings(title="Django developer", description="blablabla", address="Minsk", salary=1000, skills=[
        AddRequiredSkills(
            skill_name="Python", level=1, years_of_experience=1
        ),
        AddRequiredSkills(
            skill_name="Django", level=1, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="Developer", description="blablabla", address="Minsk", salary=2000, skills=[
        AddRequiredSkills(
            skill_name="C++", level=0, years_of_experience=1
        ),
        AddRequiredSkills(
            skill_name="Git", level=1, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="Java developer", description="blablabla", address="Minsk", salary=1000, skills=[
        AddRequiredSkills(
            skill_name="Java", level=1, years_of_experience=2
        ),
        AddRequiredSkills(
            skill_name="Docker", level=0, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="Junior JavaScript developer", description="blablabla", address="Minsk", salary=500, skills=[
        AddRequiredSkills(
            skill_name="JavaScript", level=0, years_of_experience=1
        ),
        AddRequiredSkills(
            skill_name="SQL", level=0, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="Ruby developer", description="blablabla", address="Minsk", salary=500, skills=[
        AddRequiredSkills(
            skill_name="Ruby", level=0, years_of_experience=1
        ),
        AddRequiredSkills(
            skill_name="SQL", level=0, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="C developer", description="blablabla", address="Minsk", salary=1000, skills=[
        AddRequiredSkills(
            skill_name="C++", level=1, years_of_experience=2
        ),
        AddRequiredSkills(
            skill_name="C", level=0, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="Junior developer", description="blablabla", address="Minsk", salary=1500, skills=[
        AddRequiredSkills(
            skill_name="Python", level=1, years_of_experience=2
        ),
        AddRequiredSkills(
            skill_name="Docker", level=0, years_of_experience=1
        )
    ]
    ),
    AddJobOpenings(title="JavaScript developer", description="blablabla", address="Minsk", salary=500, skills=[
        AddRequiredSkills(
            skill_name="JavaScript", level=1, years_of_experience=1
        ),
        AddRequiredSkills(
            skill_name="Node.js", level=0, years_of_experience=1
        )
    ]
    )
    ]


async def create_if_the_database_is_empty():
    """
    Create all tables.
    """
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

    if not (CandidatesDB.__tablename__ in tables and CandidatesSkillsDB.__tablename__ in tables and
            JobOpeningsDB.__tablename__ in tables and RequiredSkillsDB.__tablename__ in tables):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        for i in candidates:
            await add_model_db(model=i, orm_table_class=CandidatesDB, foreign_orm_table_class=CandidatesSkillsDB)
        for x in job_openings:
            await add_model_db(model=x, orm_table_class=JobOpeningsDB, foreign_orm_table_class=RequiredSkillsDB)
