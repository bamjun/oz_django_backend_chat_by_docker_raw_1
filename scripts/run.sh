#!/bin/sh

set -e


python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

daphne -b 0.0.0.0 -p 9000 app.route:application

# uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi:application



