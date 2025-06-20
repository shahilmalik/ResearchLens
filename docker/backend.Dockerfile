# docker/backend.Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ /app

CMD ["gunicorn", "researchlens.wsgi:application", "--bind", "0.0.0.0:8000"]
