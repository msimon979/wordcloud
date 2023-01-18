web := wordcloud-web-1

connect_web:
	docker exec -ti $(web) bash

shell:
	docker exec -ti $(web) sh -c "python manage.py shell"

migrate:
	docker exec -ti $(web) sh -c "python manage.py migrate"

makemigrations:
	docker exec -ti $(web) sh -c "python manage.py makemigrations"

createsuperuser:
	docker exec -ti $(web) sh -c "python manage.py createsuperuser --username $(username) --email $(email)"

lint:
	docker exec -ti $(web) sh -c "isort . && black . && autoflake --remove-all-unused-imports -i -r ."

start_app:
	docker-compose up -d db web

prune_docker:
	docker system prune -a && docker volume prune

init:
	docker-compose build && docker-compose up && docker exec -ti $(web) sh -c "python manage.py migrate" && docker-compose logs -f

tests:
	docker exec -ti $(web) sh -c "pytest ."