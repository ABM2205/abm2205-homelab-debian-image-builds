from os import path
from pyinfra import host, local
from pyinfra.facts import docker
from pyinfra.operations import apt, files, git, pip, server, systemd




try:
    portainer_is_running = host.get_fact( docker.DockerContainer, "portainer")[0]["State"]["Running"]
except IndexError:
    portainer_is_running = False

if not portainer_is_running:
    server.shell("sudo docker volume create portainer_data")

    docker_start = '''
    docker run -d \
        -p 8000:8000 \
        -p 9443:9443 \
        --name portainer \
        --restart=always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v portainer_data:/data portainer/portainer-ce:latest
    '''
    server.shell(docker_start)
