FROM python:3.11-alpine

RUN mkdir /dream_job

WORKDIR /dream_job

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "main:my_job", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]