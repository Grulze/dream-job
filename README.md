# My Dream Job API

This project is a RESTful API designed for managing job openings and candidates.
It is built with FastAPI and supports asynchronous operations, caching with Redis, and data storage in PostgreSQL.

## Quick Start

### Installation

**Clone the repository**:
   ```sh
   git clone https://github.com/Grulze/dream-job
   ```

### Start with Docker

1. **Before Starting**:
    Make sure you have the following installed on your local machine:
   - [Docker](https://www.docker.com/)

2. **Build Docker containers**:
   Run the following command to build the Docker containers for the app, PostgreSQL, and Redis.
   ```sh
   docker compose build
   ```

3. **Start the services**:
   Bring up the application and the associated services (PostgreSQL and Redis) using Docker Compose.
   ```sh
   docker compose up
   ```

4. **Stopping the services**:
   To stop the application and services, press `Ctrl+C` in the terminal where app is running, or run:
    ```sh
    docker compose down
    ```
   
### Start without Docker

1. **Before Starting**:
   Make sure you have the following installed on your local machine:
   - [PostgreSQL](https://www.postgresql.org)
   - [Redis](https://redis.io)

2. **Check the parameters**:
   Check the settings for connecting the services, and if they do not match, edit them.
   ```sh
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASS=postgres
   
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

3. **Installing dependencies**:
   Run the command.
   ```sh
   pip install -r requirements.txt
   ```

4. **Start the services**:
   Bring up the associated services (PostgreSQL and Redis).
   And then run the application.
   ```sh
   uvicorn core.main:my_job
   ```
   
5. **Stopping the services**:
   To stop the application and services, press `Ctrl+C` in the terminal where app is running.


### The application will now be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

**Access API documentation**:
   FastAPI provides interactive API documentation, which can be accessed at:
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)



# API Endpoints

## Project Foreword

The search is configured to be case-insensitive.
The skill level, search status, and education level are stored as numeric values, allowing for easy modification of
their labels without the need to alter the database. This also enables the use of mathematical functions on these
fields. Using a separate list, we can display the desired string representation.

### Candidate and Job Opening Matching (SelectionOfCandidatesAndJobOpenings)

#### 1. Find Candidates Matching a Job Opening
- **URL**: `"GET /api/v1/job-openings/{id}/selection`
- **Parameters** (query):
  - `id` (int) — Job Opening ID.
  - `limit` (optional, int) — quantity of objects to return (default - 10).
  - `page` (optional, int) — group number (default - 0).
  - `sorting_from` (optional, str (only 'lower' or 'upper')) - parameter by which sorting will be performed, 'lower' -
  from less qualified, 'upper' - from more qualified (default - 'lower').
  - Example: `"GET /api/v1/job-openings/1/selection?limit=10&page=0&sorting_from=lower`


#### 2. Find Job Openings Matching a Candidate’s Skills
- **URL**: `"GET /api/v1/candidates/{id}/selection`
- **Parameters** (query):
  - `id` (int) — Candidate ID.
  - `limit` (optional, int) — quantity of objects to return (default - 10).
  - `page` (optional, int) — group number (default - 0).
  - `sorting_from` (optional, str (only 'lower' or 'upper')) - parameter by which sorting will be performed, 'lower' -
  from less qualified, 'upper' - from more qualified (default - 'lower').
  - Example: `"GET /api/v1/candidates/1/selection?limit=10&page=0&sorting_from=upper`



### Candidates

#### 1. Get All Candidates
- **URL**: `GET /api/v1/candidates`
- **Parameters** (query):
  - `limit` (optional, int) — quantity of objects to return (default - 10).
  - `page` (optional, int) — group number (default - 0).
  - Example: `GET /api/v1/candidates?limit=10&page=0`

#### 2. Get Candidate by ID
- **URL**: `GET /api/v1/candidates/{id}`
- **Parameters** (path):
  - `id` (int) — Candidate ID.

#### 3. Create a New Candidate
- **URL**: `POST /api/v1/candidates`
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "second_name": "Doe",
    "age": 30,
    "city": "New York",
    "desired_position": "Software Engineer",
    "education_degree": 4,
    "working_experience": "3 years at ABC Corp",
    "about_oneself": "Experienced in backend development",
    "published": true,
    "skills" (optional) : [
      {
        "skill_name": "C++",
        "level": 2,
        "years_of_experience": 5,
        "last_used_year": 2024
      },
      {
  
      ...
  
      }...
    ]
  }
  ```
  
#### 4. Update Candidate by ID (PUT)
- **URL**: `PUT /api/v1/candidates/{id}`
- **Parameters** (path):
  - `id` (int) — Candidate ID.
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "second_name": "Doe",
    "age": 30,
    "city": "New York",
    "desired_position": "Software Engineer",
    "education_degree": 4,
    "working_experience": "3 years at ABC Corp",
    "about_oneself": "Experienced in backend development",
    "published": true
  }
  ```

#### 5. Update Candidate by ID (PATCH)
- **URL**: `PATCH /api/v1/candidates/{id}`
- **Parameters** (path):
  - `id` (int) — Candidate ID.
- **Request Body** (include only fields you want to update):

#### 6. Delete Candidate by ID
- **URL**: `DELETE /api/v1/candidates/{id}`
- **Parameters** (path):
  - `id` (int) — Candidate ID.



### Candidate Skills

#### 1. Get All Skills of a Candidate
- **URL**: `GET /api/v1/candidates/{id}/skills`
- **Parameters** (path):
  - `id` (int) — Candidate ID.

#### 2. Get Candidate Skill by Skill ID
- **URL**: `GET /api/v1/candidates/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.

#### 3. Add a Skills to a Candidate
- **URL**: `POST /api/v1/candidates/{id}/skills`
- **Parameters** (path):
  - `id` (int) — Candidate ID.
- **Request Body**:
  ```json
  [
     {
       "skill_name": "C++",
       "level": 2,
       "years_of_experience": 5,
       "last_used_year": 2024
     },
     {
 
     ...
 
     }...
  ]
  ```
  
#### 4. Update Candidate Skill by Skill ID (PUT)
- **URL**: `PUT /api/v1/candidates/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.
- **Request Body**:
  ```json
  {
    "skill_name": "C++",
    "level": 2,
    "years_of_experience": 5,
    "last_used_year": 2024
  }
  ```

#### 5. Update Candidate Skill by Skill ID (PATCH)
- **URL**: `PATCH /api/v1/candidates/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.
- **Request Body** (include only fields you want to update):

#### 6. Delete Candidate Skill by Skill ID
- **URL**: `DELETE /api/v1/candidates/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.



### Job Openings

#### 1. Get All Job Openings
- **URL**: `GET /api/v1/job-openings`
- **Parameters** (query):
  - `limit` (optional, int) — quantity of objects to return (default - 10).
  - `page` (optional, int) — group number (default - 0).
  - Example: `GET /api/v1/job-openings?limit=10&page=0`

#### 2. Get Job Opening by ID
- **URL**: `GET /api/v1/job-openings/{id}`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.

#### 3. Create a New Job Opening
- **URL**: `POST /api/v1/job-openings`
- **Request Body**:
  ```json
  {
    "title": "Backend Developer",
    "description": "Position for backend development with Python",
    "address": "New York",
    "salary": 90000,
    "skills" (optional) : [
      {
        "skill_name": "C++",
        "level": 2,
        "years_of_experience": 5
      },
      {
  
      ...
  
      }...
    ]
  }
  ```
  
#### 4. Update Job Opening by ID (PUT)
- **URL**: `PUT /api/v1/job-openings/{id}`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.
- **Request Body**:
  ```json
  {
    "title": "Backend Developer",
    "description": "Position for backend development with Python",
    "address": "New York",
    "salary": 90000
  }
  ```

#### 5. Update Job Opening by ID (PATCH)
- **URL**: `PATCH /api/v1/job-openings/{id}`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.
- **Request Body** (include only fields you want to update):

#### 6. Delete Job Opening by ID
- **URL**: `DELETE /api/v1/job-openings/{id}`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.



### Job Opening Skills

#### 1. Get All Skills of a Job Opening
- **URL**: `GET /api/v1/job-openings/{id}/skills`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.

#### 2. Get Job Opening Skill by Skill ID
- **URL**: `GET /api/v1/job-openings/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.

#### 3. Add a Skills to a Job Opening
- **URL**: `POST /api/v1/job-openings/{id}/skills`
- **Parameters** (path):
  - `id` (int) — Job Opening ID.
- **Request Body**:
  ```json
  [
     {
       "skill_name": "C++",
       "level": 2,
       "years_of_experience": 5
     },
     {
 
     ...
 
     }...
  ]
  ```


#### 4. Update Job Opening Skill by Skill ID (PUT)
- **URL**: `PUT /api/v1/job-openings/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.
- **Request Body**:
  ```json
  {
    "skill_name": "C++",
    "level": 2,
    "years_of_experience": 5
  }
  ```

#### 5. Update Job Opening Skill by Skill ID (PATCH)
- **URL**: `PATCH /api/v1/job-openings/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.
- **Request Body** (include only fields you want to update):

#### 6. Delete Job Opening Skill by Skill ID
- **URL**: `DELETE /api/v1/job-openings/skills/{id}`
- **Parameters** (path):
  - `id` (int) — Skill ID.
