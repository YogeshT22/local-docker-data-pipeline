# -------------------------------
# Purpose: Dockerfile for a Python application that interacts with PostgreSQL
# Target: Local Data Pipeline using Dockerized (PostgreSQL + Python)
# This is personal work for educational purposes.
# -------------------------------

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py .
COPY consumer.py .

# Dev note: The CMD is a default command, but will override it in docker-compose.yml
CMD ["python"]
