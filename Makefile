export PROJECT_NAME=hand-probability-calculator
export ENV?=development

ifeq (${ENV}, production)
	dc := docker-compose -f docker/docker-compose.yml
else
	dc := docker-compose -f docker/docker-compose.yml -f docker/docker-compose.development.yml
endif

dc-exec := $(dc) exec app
python-exec := $(dc-exec) pdm run

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: Makefile| sed 's/://')

setup:
	$(MAKE) "setup-$(ENV)"

setup-production: build

setup-development: build create-volumes up pdm-install-dev install-labextensions

create-volumes:
	docker volume create --name jupyter-config
	docker volume create --name venv-${PROJECT_NAME}

pdm-install-dev:
	$(dc-exec) pdm sync

install-labextensions:
	$(dc-exec) sh install_labextensions

build:
	$(dc) build $(ARGS)

up:
	$(dc) up -d

down:
	$(dc) down

stop:
	$(dc) stop

start:
	$(dc) start

erase:
	$(dc) down -v

sh:
	$(dc-exec) /bin/bash

jupyter-up:
	$(python-exec) jupyter-up

jupyter-update-password:
	$(python-exec) jupyter-update-password

