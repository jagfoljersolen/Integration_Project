## DATA INTEGRATION PROJECT (Dockerized)

## Overview

This branch provides a fully containerized setup for the Data Integration Project, which compiles and analyzes data on past and ongoing armed conflicts alongside commodity prices. 

For manual setup and more project details, see the main branch README.

## Features
The project integrates data on armed conflicts and commodity prices, offering advanced analytical and visualization tools. Key system features include:

- **1. Main dashboard**
	- Presents a summary of the number of years with commodity and conflict data, the latest available years, and the historical data range.
	- Aggregates statistics from both datasets and enables a quick overview of the database status.		
- **2. Commodity dashboard**
	- List of available commodities (e.g., oil, gas, metals, agricultural products) and visualization of their prices over time.
	- Dynamic data fetching for the selected commodity for charts and analyses.
	
- **3. Conflict dashboard**
	- Statistics on armed conflicts by year, type, and intensity level.
	- Graphical data representation.
		
- **4. REST API for dashboards**
	- API for retrieving commodity and conflict data, used by the frontend for dynamic visualizations
	
- **5. Tables and reports**
	- Browse tables with commodity data, conflict data, or their joined reports (e.g., by year).
	- Select displayed columns.
	- Search by name.
		
- **6. Data export**
	- Select data range for export.
	- Export to JSON or XML format—the user chooses the output format.
	- Export includes both raw table data and joined data (e.g., by year).
	
- **6. Correlations and visualizations**
	- Dynamically generate charts of commodity prices against the number of conflicts over the years.
	- Automatically generate a heatmap of correlations between the number and intensity of conflicts and the prices of selected commodities
   
- **7. User management**
	- User registration, login, and logout.
	- Access to key features requires authorization (login-protected views).
	- Admin panel available at http://127.0.0.1:8000/admin/
		
- **8. Transactions with isolation level control**
	- Transaction mechanisms with the ability to set isolation level, read-only mode, and query timeout.
	
	

### **Technologies**
- **Backend:** Django (Python)
- **Frontend:** JavaScript (Django templates)
- **Database:** PostgreSQL
- **API:** Django REST Framework (REST API)
- **Authentication:** Django Auth, Django Admin Panel
- **ORM:** Django ORM
- **Containerization:** Docker, Docker Compose

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


