build:
	docker-compose build fasty

migrate:
	docker-compose run fasty alembic upgrade head

up:
	docker-compose up
