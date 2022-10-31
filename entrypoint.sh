#!/bin/sh

if [ "1" = "1" ]
then
  python manage.py makemigrations users
  python manage.py migrate users
  python manage.py makemigrations studies
  python manage.py migrate studies
  python manage.py migrate

  python manage.py create_superuser
  python manage.py create_users
  python manage.py populate_db
fi

exec "$@"