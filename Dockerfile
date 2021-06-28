FROM python:3.8.10-buster

ADD requirements.txt /app/requirements.txt

RUN set -ex\
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ADD . .

CMD python manage.py makemigrations && python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000