from os import path

from pyinfra import host, local
from pyinfra.operations import apt, files, git, pip, server, systemd

apt.packages(
    name="Install required apt packages",
    packages=["python3", "python3-dev", "python3-pip", "git"],
    update=True,
    cache_time=3600,
)

if host.data.get("is_portainer"):
    local.include(filename=path.join("tasks", "portainer_install.py"))

if host.data.get("is_nginx_proxy_manager"):
    local.include(filename=path.join("tasks", "nginx_proxy_manager_install.py"))

if host.data.get("is_ldap"):
    local.include(filename=path.join("tasks", "docker_install.py"))
    local.include(filename=path.join("tasks", "ldap_install.py"))