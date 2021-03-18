container = web

init:
	docker-compose -f compose/docker-compose.yaml build \
	&& docker-compose -f compose/docker-compose.yaml run $(container) python manage.py migrate \
	&& docker-compose -f compose/docker-compose.yaml run $(container) python manage.py loaddata organizations \
	&& docker-compose -f compose/docker-compose.yaml run $(container) python manage.py crawl \
	&& docker-compose -f compose/docker-compose.yaml run $(container) python manage.py tokenizer \
	&& docker-compose -f compose/docker-compose.yaml run $(container) python manage.py wordcloud \

up:
	docker-compose -f compose/docker-compose.yaml up

bash:
	docker-compose -f compose/docker-compose.yaml run $(container) bash

requirements:
	docker-compose -f compose/docker-compose.yaml run $(container) pip freeze > planes/requirements.txt