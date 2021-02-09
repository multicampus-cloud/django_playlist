#!/bin/bash -x

sleep 15

python3.8 manage.py migrate

/usr/local/bin/docker-entrypoint.sh &

sleep 25

python3.8 manage.py search_index -f --rebuild

sleep 5

python3.8 manage.py runserver 0:8000