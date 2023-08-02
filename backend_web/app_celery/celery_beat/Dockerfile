FROM python:3.10


ENV PYTHONDONTWRITEBYTE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend_web
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "-A", "app_celery", "beat", "-l", "error", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
