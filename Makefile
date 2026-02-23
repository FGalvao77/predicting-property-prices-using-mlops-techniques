# Convenience Makefile for Docker Compose

COMPOSE=docker compose

.PHONY: build up upd logs-api logs-web down

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

upd:
	$(COMPOSE) up -d

logs-api:
	$(COMPOSE) logs -f api

logs-web:
	$(COMPOSE) logs -f web

down:
	$(COMPOSE) down
