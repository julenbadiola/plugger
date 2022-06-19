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

.PHONY: dev
dev: down ## Starts development containers
	docker-compose up -d

.PHONY: swarm
swarm: down ## Starts development containers
	docker stack rm stackdemo
	(echo -e "version: '3.8'\n";  docker compose -f docker-compose.yml -f docker-compose.swarm.yml --env-file .env.swarm config) | docker stack deploy --compose-file - stackdemo

.PHONY: prod
prod: down ## Starts production containers
	docker-compose up  -f docker-compose.yml -f docker-compose.prod.yml -d

.PHONY: documentation
documentation: ## Build documentation
	cd docs && ./build.sh

.PHONY: test
test: ## Starts tests
	# docker run --rm -it --name testing -v $(pwd):/app badiolajulen/plugger:master python3 manage.py test
	docker exec plugger python3 manage.py test