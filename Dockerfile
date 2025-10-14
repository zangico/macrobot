FROM python:3.13-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src:/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 60010

CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py"]