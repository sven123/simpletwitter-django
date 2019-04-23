# simpletwitter-django
simpletwitter exercise now in django

Simple twitter using django rest framework

## Install
pip install -r requirements.txt

## Try it
The database is bundled so:

python manage.py runserver

Point your browser to: http://127.0.0.1:8000/

The summary API
http://127.0.0.1:8000/tweets/summary/

Takes query parameter timeframe, valid values are year, month, day.


## Test

python manage.py test
