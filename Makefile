migrate:
	uv run src/manage.py makemigrations user schedule calculation
	uv run src/manage.py migrate

start-docker:
	docker compose -f calc-local-dev/docker-compose-local-dev.yml up main-db -d
	docker compose -f calc-local-dev/docker-compose-local-dev.yml up postgres -d

stop-docker:
	docker compose -f calc-local-dev/docker-compose-local-dev.yml stop

rm-docker:
	docker compose -f calc-local-dev/docker-compose-local-dev.yml down -v

setup-db: start-docker
	@echo "Waiting for databases to be ready..."
	sleep 10
	uv run src/manage.py migrate
	@echo "Database setup complete!"