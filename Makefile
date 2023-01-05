web := sure-assignment-web-1

shell:
	docker exec -ti $(web) sh -c "python manage.py shell"

migrate:
	docker exec -ti $(web) sh -c "python manage.py migrate"

makemigrations:
	docker exec -ti $(web) sh -c "python manage.py makemigrations"

createsuperuser:
	docker exec -ti $(web) sh -c "python manage.py createsuperuser --username $(username) --email $(email)"

lint:
	docker exec -ti $(web) sh -c "isort . && black ."
