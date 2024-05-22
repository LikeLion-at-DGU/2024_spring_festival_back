FROM python:3.11

WORKDIR /app

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG_VALUE}
ENV DJANGO_DEPLOY=${DJANGO_DEPLOY}

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN pip install gunicorn

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 festival.wsgi:application"]