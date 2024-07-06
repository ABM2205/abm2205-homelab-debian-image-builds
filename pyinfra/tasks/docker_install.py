from pyinfra import host, local
from pyinfra.operations import apt, systemd, server
from pyinfra.facts.deb import DebPackages
from pyinfra.facts.server import LinuxName, LinuxDistribution

docker_version = "5:26.1.3-1~ubuntu.22.04~jammy"

def is_ubuntu(major_version=None):
    if host.get_fact(LinuxName) == "Ubuntu":
        if major_version:
            return int(major_version) == host.get_fact(LinuxDistribution)["major"]
        return True
    else:
        return False

def ubuntu_22_install():
    apt.packages(
        name="Clean up old packages before installing docker",
        packages=[
            "docker.io",
            "docker-doc",
            "docker-compose",
            "docker-compose-v2",
            "podman-docker", 
            "containerd"
            "runc",
            "docker-ce",
            "containerd.io",
            "docker-ce-cli",
            "docker-buildx-plugin",
            "docker-compose-plugin",
        ],
        present=False,
    )
    apt.packages(
        name="Install Depedencies for install process",
        packages=["apt-transport-https", "curl"],
        update=True,
        cache_time=3600,
    )
    server.shell(
        name="set up dockers apt repo for ubuntu",
        commands=[
            '''
            sudo apt-get update;
            sudo apt-get install ca-certificates curl;
            sudo install -m 0755 -d /etc/apt/keyrings;
            sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc;
            sudo chmod a+r /etc/apt/keyrings/docker.asc;
            echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
            $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
            sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            sudo apt-get update
            ''',
            ],
    )
    
    apt.packages(
        name="Install Docker Community Edition",
        packages=[
            f"docker-ce={docker_version}",
            "containerd.io=1.6.24-1",
            f"docker-ce-cli={docker_version}",
            "docker-buildx-plugin",
            "docker-compose-plugin"],
        update=True,
        cache_time=3600,
    )
    systemd.service(
        name="Enable Docker service",
        service="docker",
        running=True,
        enabled=True,
    )

if is_ubuntu(major_version="22"):
    try:
        docker_installed = docker_version in str(host.get_fact(DebPackages)["docker-ce"])
    except KeyError:
        docker_installed = False
    if docker_installed:
        print("Docker already installed, skipping...")
    else:
        ubuntu_22_install()

if is_ubuntu():
    server.group(name="Ensure docker group exists", group="docker", present=True)
    server.shell(commands=['sudo usermod -aG docker amccann'])
