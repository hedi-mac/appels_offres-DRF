# Variables
DOCKER_COMPOSE = @docker compose
DOCKER_EXEC = @docker exec appels_offres
DOCKER_MANAGE = $(DOCKER_EXEC) python ao_website/manage.py
PIP = pip

# Start the docker containers
start:
	$(DOCKER_COMPOSE) up --build

# Default target
up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

# Database migration
migrate:
	$(DOCKER_MANAGE) makemigrations
	$(DOCKER_MANAGE) migrate

# Run tests
test:
	$(DOCKER_MANAGE) test apps.appelsoffres.tests.test_marche_api

# Clean up
clean:
	$(DOCKER_COMPOSE) down -v

pre-commit-all:
	$(DOCKER_EXEC) pre-commit run --all-files

fake-acheteurs:
	$(DOCKER_MANAGE) fake_acheteurs

generate_departements:
	$(DOCKER_MANAGE) generate_departements

generate_competences:
	$(DOCKER_MANAGE) generate_competences

generate_pieces:
	$(DOCKER_MANAGE) generate_pieces

generate_procedures:
	$(DOCKER_MANAGE) generate_procedures

generate_codes_cpv:
	$(DOCKER_MANAGE) generate_codes_cpv

generate_type_marche:
	$(DOCKER_MANAGE) generate_type_marche

fake-marches: generate_type_marche generate_codes_cpv generate_departements generate_competences generate_pieces generate_procedures fake-acheteurs
	$(DOCKER_MANAGE) fake_marches
