release: python manage.py migrate
web: bin/start-pgbouncer-stunnel gunicorn contaq_io.wsgi --log-file -
worker: celery -A contaq_io worker -l INFO
