#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import webbrowser

# Function to check if a command exists
def command_exists(cmd):
    return subprocess.call(f"command -v {cmd} > /dev/null 2>&1", shell=True) == 0

# Check if Docker is installed
def check_docker():
    if not command_exists('docker'):
        print("Docker is not installed. Installing Docker...")
        subprocess.run("curl -fsSL https://get.docker.com | sh", shell=True)
        subprocess.run("sudo usermod -aG docker $USER", shell=True)
        print("Docker installed successfully.")

# Check if Docker Compose is installed
def check_docker_compose():
    if not command_exists('docker-compose'):
        print("Docker Compose is not installed. Installing Docker Compose...")
        subprocess.run("sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose", shell=True)
        subprocess.run("sudo chmod +x /usr/local/bin/docker-compose", shell=True)
        print("Docker Compose installed successfully.")

# Create a WordPress site using Docker Compose
def create_wordpress_site(site_name):
    print(f"Creating WordPress site: {site_name}")
    subprocess.run(f"mkdir -p {site_name}", shell=True)
    with open(f"{site_name}/docker-compose.yml", "w") as compose_file:
        compose_file.write(f"""version: "3"
services:
  nginx:
    image: nginx:latest
    ports:
      - "8000:80"
    volumes:
      - ./{site_name}/nginx/conf.d:/etc/nginx/conf.d
      - ./{site_name}/nginx/html:/var/www/html
    depends_on:
      - php
    networks:
      - lemp_network

  php:
    image: php:latest
    volumes:
      - ./{site_name}/php:/var/www/html
    networks:
      - lemp_network

  mysql:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - {site_name}_db_data:/var/lib/mysql
    networks:
      - lemp_network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    ports:
      - "8080:80"
    environment:
      PMA_HOST: mysql
      MYSQL_ROOT_PASSWORD: rootpassword
    depends_on:
      - mysql
    networks:
      - lemp_network

volumes:
  {site_name}_db_data:

networks:
  lemp_network:
""")
    subprocess.run(f"mkdir -p {site_name}/nginx/conf.d {site_name}/nginx/html {site_name}/php", shell=True)
    with open(f"{site_name}/nginx/conf.d/default.conf", "w") as nginx_conf:
        nginx_conf.write(f"""server {{
    listen 80;
    server_name localhost;

    root /var/www/html;
    index index.php index.html;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    location ~ \.php$ {{
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }}
}}
""")

# Enable the site (start containers)
def enable_site(site_name):
    print(f"Enabling WordPress site: {site_name}")
    subprocess.run(f"cd {site_name} && docker-compose up -d", shell=True)
    print("Waiting for the site to be up and healthy...")
    while subprocess.call(f"docker-compose exec php curl -s http://localhost:8000 > /dev/null", shell=True) != 0:
        time.sleep(5)
    subprocess.run(f"echo '127.0.0.1 example.com' | sudo tee -a /etc/hosts", shell=True)
    print(f"WordPress site {site_name} is now running at http://example.com:8000")
    print("PhpMyAdmin is accessible at http://localhost:8080")
    input("Press Enter to open http://example.com in your default web browser...")
    webbrowser.open("http://example.com:8000")

# Disable the site (stop containers)
def disable_site(site_name):
    print(f"Disabling WordPress site: {site_name}")
    subprocess.run(f"cd {site_name} && docker-compose down", shell=True)
    subprocess.run(f"sudo sed -i '/127.0.0.1 example.com/d' /etc/hosts", shell=True)
    print(f"WordPress site {site_name} has been disabled.")

# Delete the site (stop containers, remove local files)
def delete_site(site_name):
    print(f"Deleting WordPress site: {site_name}")
    subprocess.run(f"cd {site_name} && docker-compose down", shell=True)
    subprocess.run(f"sudo sed -i '/127.0.0.1 example.com/d' /etc/hosts", shell=True)
    subprocess.run(f"rm -rf {site_name}", shell=True)
    print(f"WordPress site {site_name} has been deleted.")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./script.py <subcommand> <site_name>")
        sys.exit(1)

    subcommand = sys.argv[1]
    site_name = sys.argv[2]

    if subcommand == "check":
        check_docker()
        check_docker_compose()
    elif subcommand == "create":
        check_docker()
        check_docker_compose()
        create_wordpress_site(site_name)
    elif subcommand == "enable":
        enable_site(site_name)
    elif subcommand == "disable":
        disable_site(site_name)
    elif subcommand == "delete":
        delete_site(site_name)
    else:
        print("Invalid subcommand. Available subcommands: check, create, enable, disable, delete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
