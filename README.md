# Manage WordPress Site using LEMP Stack (Docker)

This Python script allows you to manage a WordPress site running on a LEMP stack using Docker containers.

## Prerequisites

Make sure you have the following tools installed on your system:

1. Docker: [Install Docker](https://docs.docker.com/get-docker/)
2. Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Usage

### 1. Check and Install Docker and Docker Compose

Run the following command to check if Docker and Docker Compose are installed on your system:

```bash
./manage_wordpress.py check

```

### 2. Create a WordPress Site
To create a new WordPress site, provide the desired site name as an argument:

```bash
./manage_wordpress.py create <site_name>

```

### 3. Enable (Start) the WordPress Site
To enable (start) the WordPress site and make it accessible, use the following command:

```bash
./manage_wordpress.py enable <site_name>

```

This command will start the LEMP stack containers and add an entry to /etc/hosts to map example.com to localhost. It will also open http://example.com:8000 in your default web browser once the site is up and running.


### 4. Disable (Stop) the WordPress Site
To disable (stop) the WordPress site, use the following command:

```bash
./manage_wordpress.py disable <site_name>

```

This command will stop the LEMP stack containers and remove the entry from /etc/hosts.

### 5. Delete the WordPress Site
To completely delete the WordPress site, including stopping the containers and removing local files, use the following command:

```bash
./manage_wordpress.py delete <site_name>

```

This command will stop the LEMP stack containers, remove the entry from /etc/hosts, and delete the site directory.

