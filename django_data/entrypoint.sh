if [ $DEBUG = "True" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
fi