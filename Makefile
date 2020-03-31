NAME=fastapi_docker

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose down

status:
	docker-compose ps

run-no:
	docker-compose build --no-cache
	docker-compose up -d

exec:
	docker-compose exec web bash

log:
	docker-compose logs -f web


#heroku run bash

deploy:
	heroku git:remote -a sheltered-mountain-37347
	heroku container:login
	heroku container:push web
	heroku container:release web

logs:
	heroku logs

