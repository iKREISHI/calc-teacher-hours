migrate:
	uv run src/manage.py makemigrations user
	uv run src/manage.py migrate