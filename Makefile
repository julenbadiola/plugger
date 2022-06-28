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

############ 
# Environments
############

.PHONY: dev
dev: down ## Starts development containers
	docker-compose up -d

.PHONY: swarm
swarm: down ## Starts development containers in swarm mode
	docker stack rm stackdemo
	(echo -e "version: '3.8'\n";  docker compose -f docker-compose.yml -f docker-compose.swarm.yml --env-file .env.swarm config) | docker stack deploy --compose-file - stackdemo

.PHONY: prod
prod: down ## Starts production containers
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

.PHONY: testing
testing: down ## Starts production containers
	docker-compose -f docker-compose.test.yml up -d

############ 
# DOCUMENTATION
############

.PHONY: documentation
documentation: ## Build documentation
	cd docs && ./build.sh

############ 
# TESTING
############

.PHONY: test-unit
test-unit: ## Starts unit tests
	docker exec plugger python3 manage.py test --exclude-tag=e2e

.PHONY: test-e2e
test-e2e: ## Starts e2e tests after starting selenium containers
	docker exec plugger python3 manage.py test --tag=e2e

.PHONY: test-coverage
test-coverage: ## Starts tests with coverage measuring
	docker exec plugger ./test.sh