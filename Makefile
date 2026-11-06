build:
	docker compose build fasty

migrate:
	docker compose run --rm fasty alembic upgrade head

up:
	docker compose up
