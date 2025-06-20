FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt

# Install netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ /app

# Wait for PostgreSQL and start Celery with solo pool
CMD ["sh", "-c", "until nc -z postgres 5432; do sleep 1; done; celery -A researchlens worker -l info --pool=solo"]
