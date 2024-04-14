
docker_compose_path = "docker-compose.yaml"

build:
	docker compose -f $(docker_compose_path) build

run:
	docker compose -f $(docker_compose_path) up

down:
	docker compose -f $(docker_compose_path) down
