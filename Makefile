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
	heroku container:push web
	heroku container:release web

logs:
	heroku logs

