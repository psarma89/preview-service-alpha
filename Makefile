SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help setup build up down reset \
        migrate migrations test lint fmt check \
        seed seed-nuke shell-db

AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text 2>/dev/null)
AWS_REGION     ?= us-east-1
ECR_REPO       ?= $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/preview-service-alpha

# Load .env.local if it exists
ENV_FILE := $(shell [ -f .env.local ] && echo "--env-file .env.local")
DC := docker compose $(ENV_FILE)

# ============================================
# Help
# ============================================

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# Local Development
# ============================================

setup: build migrate seed ## First-time setup: build, migrate, and seed

build: ## Build Docker image
	$(DC) build

up: ## Start the service
	$(DC) up

down: ## Stop the service
	$(DC) down

reset: ## Stop and wipe database volume
	$(DC) down -v

# ============================================
# Database
# ============================================

migrate: ## Run migrations
	$(DC) run --rm migrate

migrations: ## Auto-generate a new migration (MESSAGE= required)
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Error: MESSAGE is required. Usage: make migrations MESSAGE=\"add foo\""; \
		exit 1; \
	fi
	$(DC) run --rm migrate alembic revision --autogenerate -m "$(MESSAGE)"

seed: ## Seed the database with sample data
	$(DC) run --rm app python -m scripts.seed

seed-nuke: ## Wipe and re-seed
	$(DC) run --rm app python -m scripts.seed --nuke

shell-db: ## Open a psql shell
	$(DC) exec db psql -U postgres -d appdb

# ============================================
# Quality
# ============================================

test: ## Run tests
	python -m pytest tests/ -v

lint: ## Lint with ruff
	ruff check .

fmt: ## Format with ruff
	ruff format .
	ruff check --fix .

check: lint test ## Lint + test

# ============================================
# CI/CD
# ============================================

ci-migrate: ## Run migrations directly (expects DATABASE_URL)
	alembic upgrade head

ecr-login: ## Login to ECR
	aws ecr get-login-password --region $(AWS_REGION) | \
		docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

push: ecr-login ## Build and push to ECR (TAG= required)
	@if [ -z "$(TAG)" ]; then \
		echo "Error: TAG is required. Usage: make push TAG=feat-xyz"; \
		exit 1; \
	fi
	docker build -t $(ECR_REPO):$(TAG) .
	docker push $(ECR_REPO):$(TAG)
