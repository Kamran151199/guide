run:
	docker-compose -f  docker-compose.yml up
run-build:
	docker-compose -f docker-compose.yml up --build
stop:
	docker-compose -f docker-compose.yml stop
down:
	docker-compose -f docker-compose.yml down
superuser:
	docker-compose -f docker-compose.yml exec splunk-dummy-api python manage.py createsuperuser --noinput
collect-static:
	docker-compose -f ./docker-compose.yml run splunk-dummy-api python manage.py collectstatic
tls:
	docker-compose -f ./docker-compose.cert.yml up
run-prod:
	docker-compose -f ./docker-compose.yml -f docker-compose.prod.yml up -d
rm-prod:
	docker-compose -f docker-compose.prod.yml rm
run-build-prod:
	docker-compose -f docker-compose.prod.yml up -d --build
stop-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml stop
superuser-prod:
	docker-compose -f docker-compose.prod.yml exec splunk-dummy-api python manage.py createsuperuser --noinput
collect-static-prod:
	docker-compose -f ./docker-compose.prod.yml run splunk-dummy-api python manage.py collectstatic
test:
	cd src && pytest .
black:
	black src
install:
	pip install -r ./src/requirements.txt
.PHONY: run run-prod run-build run-build-prod stop stop-prod down superuser superuser-prod collect-static collect-static-prod tls
