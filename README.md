## DATA INTEGRATION PROJECT (Dockerized)

## Overview

This branch provides a fully containerized setup for the Data Integration Project, which compiles and analyzes data on past and ongoing armed conflicts alongside commodity prices. 

For manual setup and more project details, see the main branch README.

## Prerequisites
- Docker
- Docker Compose

## Quick Start

## 1. Clone the repository and switch to the docker branch:

	git clone https://github.com/jagfoljersolen/data-integration-project.git
	cd data-integration-project
	git checkout docker

## 2. Copy the environment file template:

	cp .env.example .env

	(Edit .env if you need to change default credentials or ports.)
 # Create Docker secrets for the database (required for Compose):
	echo "integration" > db_password.txt
	echo "db_user" > db_user.txt
	echo "integration_db" > db_name.txt

## 3. Build and start the containers:

	docker compose up --build

## 4. Initialize the database (in a new terminal):

	docker compose exec web python manage.py migrate
	docker compose exec web python manage.py import_commodity_with_units data/commodity_with_units.csv
	docker compose exec web python manage.py import_conflicts data/conflicts.csv --batch-size 1000

## 5. (Optional) Create an admin user:

    docker compose exec web python manage.py createsuperuser

## 6. Access the application:

Main app: **http://localhost:8000/**

Admin panel: http://localhost:8000/admin/

Configuration

    Environment variables:
    Edit the .env file to adjust database credentials, secret keys, etc.

    Data volumes:
    Database data is persisted in a Docker volume (pgdata).

Stopping and Cleaning Up

    Stop containers:
    docker compose down

    Stop and remove containers, networks, and volumes:
    docker compose down -v


