#!/bin/bash

echo "Iniciando Gunicorn..." >> /tmp/startup.log
/home/vinicius/.local/bin/pipenv run gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

echo "Iniciando SSH..." >> /tmp/startup.log
ssh -L 27017:wl-compute-8-0:27017 -i ~/.ssh/wetterlab-mongodb -N vinicius@34.23.51.63 &

wait
