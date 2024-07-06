
inventory = [
    (
        "nginx_proxy_manager",
        {
            # SSH details matching the Docker container started in ./docker-start.sh
            "ssh_hostname": "proxy.amccann.io",
            "ssh_port": 22,
            "ssh_user": "amccann",
            "ssh_key": "~/.ssh/id_rsa",
            "ssh_known_hosts_file": "/dev/null",
            # This is insecure, don't use in production!
            "ssh_strict_host_key_checking": "off",
            "is_nginx_proxy_manager": True,
            "_sudo": True,
        },
    ),
]