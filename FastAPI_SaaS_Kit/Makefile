.PHONY: dev test migrate lint format

dev:
	docker compose up --build

test:
	pip install -e ".[dev]" -q && pytest -v

migrate:
	alembic upgrade head

lint:
	ruff check .

format:
	ruff format .
