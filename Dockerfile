FROM python:3-slim

ENV PYTHONUNBUFFERED=true

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

WORKDIR /app/server

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]