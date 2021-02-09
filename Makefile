container = web
folder = planes
heroku_app = planes2021

deploy:
	cp -R $(folder) ~/
	docker-compose run $(container) pip freeze > ~/$(folder)/requirements.txt
	cd ~/$(folder) && echo 'web: gunicorn planes.wsgi --workers=2 --bind=0.0.0.0:$$PORT' > Procfile \
					&& git init \
					&& heroku git:remote -a $(heroku_app) \
					&& git add . \
					&& git commit -am "deploy" \
					&& git push heroku master -f \
					&& heroku ps:scale web=1 \
					&& heroku run python manage.py migrate --app=$(heroku_app)
	sudo rm -r ~/$(folder)

init:
	docker-compose build
	docker-compose run $(container) python manage.py loaddata organizations
	docker-compose run $(container) python manage.py crawl
	docker-compose run $(container) python manage.py tokenizer
	docker-compose run $(container) python manage.py wordcloud