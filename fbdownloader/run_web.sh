#!/bin/sh

# wait for PSQL server to start
sleep 10

su -m coneser -c "python manage.py makemigrations"
su -m coneser -c "python manage.py migrate"
su -m coneser -c "python manage.py runserver 0.0.0.0:8000"
