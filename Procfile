web: PYTHONPATH=/app/src gunicorn .core.wsgi:application --bind 0.0.0.0:$PORT
worker: echo "$SSH_PRIVATE_KEY" > /app/.ssh/wetterlab-mongodb && ssh -L 27017:10.0.0.51:27017 -i /app/.ssh/wetterlab-mongodb -N vinicius@34.23.51.63
