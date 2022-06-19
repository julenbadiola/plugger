SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: down
down: ## Stops all containers
	docker-compose down --remove-orphans
	
.PHONY: build
build: ## Builds containers
	docker-compose build

.PHONY: up
up: down ## Starts development containers
	docker-compose up -d

.PHONY: test
test: ## Starts tests
	# docker run --rm -it --name testing -v $(pwd):/app badiolajulen/plugger:master python3 manage.py test
	docker exec plugger python3 manage.py test