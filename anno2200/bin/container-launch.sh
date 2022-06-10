#!/bin/bash

if [ -n ${DJANGO_SUPERUSER_USERNAME} ] && [ -n ${DJANGO_SUPERUSER_PASSWORD} ] ; then
    /opt/app/src/manage.py createsuperuser --no-input
fi

nginx -g "daemon off;"
gunicorn anno.wsgi --user www-data --bind 0.0.0.0:8000 --workers 3
