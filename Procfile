web: daphne webchatsite.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=webchatsite.settings -v2