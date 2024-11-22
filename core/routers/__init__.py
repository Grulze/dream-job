from .all_candidates_and_job_openings import router as router1
from .cr_job_openings_skills import router as router2
from .crud_candidates import router as router3
from .cr_candidates_skills import router as router4
from .crud_job_openings import router as router5
from .rud_candidates_skills import router as router6
from .rud_job_openings_skills import router as router7
from .selection_of_candidates_and_job_openings import router as router8


routers_set = (
    router1,
    router2,
    router3,
    router4,
    router5,
    router6,
    router7,
    router8,
)
