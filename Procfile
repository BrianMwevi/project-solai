web: daphne core.asgi:application 0.0.0.0:$PORT
worker: python manage.py runworker channels --settings=core.settings -v2