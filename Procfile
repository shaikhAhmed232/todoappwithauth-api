release: python manage.py migrate --settings=core.settings.production
web: gunicorn core.wsgi --log-file=-