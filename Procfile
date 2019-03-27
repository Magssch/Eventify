release: python manage.py makemigrations
release: python manage.py migrate sites
release: python manage.py migrate
web: gunicorn eventifySite.wsgi --log-file -