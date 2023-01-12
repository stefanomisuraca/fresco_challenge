#!/bin/sh

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/users.json

python manage.py runserver 0.0.0.0:8000
# uwsgi --ini ./fresco.uwsgi.ini

exec "$@"