migrate:
	uv run src/manage.py makemigrations user schedule calculation
	uv run src/manage.py migrate

start-docker:
	docker compose -f docker-compose-local-dev.yml up postgres -d

stop-docker:
	docker compose -f docker-compose-local-dev.yml stop

rm-docker:
	docker compose -f docker-compose-local-dev.yml down -v