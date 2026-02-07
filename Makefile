up:
	docker-compose up --build

load:
	docker exec -it flight_app python manage.py loaddata sample_data.json

superuser:
	docker exec -it flight_app python manage.py createsuperuser
