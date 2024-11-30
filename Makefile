pg-up:
	docker compose -f docker-compose-dev.yaml up -d

pg-down:
	docker compose -f docker-compose-dev.yaml down && docker network prune --force

al-h:
	alembic history

al-mm:
	alembic revision --autogenerate

al-uh:
	alembic upgrade heads
