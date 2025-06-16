# docker/backend.Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend/ /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "researchlens.wsgi:application", "--bind", "0.0.0.0:8000"]
