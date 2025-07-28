FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
COPY .env .env

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "main.py"]
