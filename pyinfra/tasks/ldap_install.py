from os import path
from pyinfra import host, local
from pyinfra.operations import apt, files, server
from pyinfra.facts.deb import DebPackages
from pyinfra.facts.server import LinuxName, LinuxDistribution

local.include(filename=path.join("tasks", "docker_install.py"))

#apt.packages(
#        name="Install Depedencies for install process",
#        packages=["slapd", "ldap-utils"],
#        update=True,
#        cache_time=3600,
#)

uploaded_file=files.put(
    name="update /etc/ldap/ldap.conf",
    src="config/ldap/ldap.conf",
    dest="/etc/ldap/ldap.conf"
).changed

if uploaded_file:
    server.shell(
        name="Restart slapd and recreate ldap database",
        commands=["dpkg-reconfigure slapd", "systemctl restart slapd"]
    )

docker_compose_path = "/home/amccann/docker-compose.yaml"

compose_changed = files.put(
    name="Docker compose file for Nginx Proxy Manager",
    src="scripts/ldap-ui-compose.yaml",
    dest=docker_compose_path
).changed

if compose_changed:
    server.shell(
        name="docker-compose up -d",
        commands=[
            f"docker compose -f {docker_compose_path} up -d"
        ]
    )