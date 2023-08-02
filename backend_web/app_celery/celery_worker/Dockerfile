FROM python:3.10


ENV PYTHONDONTWRITEBYTE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend_web
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
ENV CELERY_WORKER_PROCESS="True"

CMD ["python3", "-m", "celery", "-A", "app_celery", "worker", "-l", "info", "-c", "2"]
