# Build Docker Container
.PHONY: build
build:
	docker-compose up -d --build

# Run Docker Container
.PHONY: run
run:
	docker-compose up -d

# Stop all running containers
.PHONY: stop
stop:
	docker-compose down

# bash into container
.PHONY: python
python:
	docker-compose exec web bash

# get logs into container
.PHONY: logs
logs:
	docker-compose logs web
