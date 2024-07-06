from os import path
from pyinfra import local
from pyinfra.operations import files, server



local.include(filename=path.join("tasks", "docker_install.py"))

docker_compose_path = "/home/amccann/docker-compose.yaml"

files.put(
    name="Docker compose file for Nginx Proxy Manager",
    src="scripts/nginx_proxy_manager.yaml",
    dest=docker_compose_path
)

server.shell(
    name="docker-compose up -d",
    commands=[
        f"docker compose -f {docker_compose_path} up -d"
    ]
)