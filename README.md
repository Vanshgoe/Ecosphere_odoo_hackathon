# EcoSphere Odoo 18 Docker Setup

This project is configured to run as a complete Odoo 18 stack with PostgreSQL using Docker Compose.

## Prerequisites

- Docker Engine 24+
- Docker Compose v2

## Run

From the project root, start the stack with:

```bash
docker compose up --build
```

Once the containers are running, open:

- http://localhost:8069

## Useful commands

```bash
# Stop the stack
docker compose down

# Stop and remove volumes
docker compose down -v

# Follow Odoo logs
docker compose logs -f odoo
```

## Container details

- PostgreSQL service: `db`
- Odoo service: `odoo`
- Addons mounted from: `./addons`
- Odoo config file: `./odoo.conf`
