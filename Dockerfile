FROM python:3.11-alpine

RUN mkdir /dream_job

WORKDIR /dream_job

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:my_job", "--host", "0.0.0.0", "--port", "8000"]