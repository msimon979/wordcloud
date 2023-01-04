shell:
	docker exec -ti sure-assignment-web-1 sh -c "python manage.py shell"

migrate:
	docker exec -ti sure-assignment-web-1 sh -c "python manage.py migrate"

makemigrations:
	docker exec -ti sure-assignment-web-1 sh -c "python manage.py makemigrations"

createsuperuser:
	docker exec -ti sure-assignment-web-1 sh -c "python manage.py createsuperuser --username $(username) --email $(email)"
