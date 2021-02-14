container = web
folder = planes
heroku_app = planes2021

init:
	cd compose \
	&& cp env.example .env \
	&& docker-compose build \
	&& docker-compose run $(container) python manage.py migrate \
	&& docker-compose run $(container) python manage.py loaddata organizations \
	&& docker-compose run $(container) python manage.py crawl \
	&& docker-compose run $(container) python manage.py tokenizer \
	&& docker-compose run $(container) python manage.py wordcloud \

up:
	cd compose \
	&& docker-compose up

bash:
	cd compose \
	&& docker-compose run $(container) bash