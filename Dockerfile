FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src:/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


EXPOSE $PORT

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py"]