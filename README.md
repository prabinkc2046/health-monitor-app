# System Health Monitor

This project is a system health monitoring application that collects and visualizes CPU usage, memory usage, and disk usage over time. It consists of two components: the Flask web application and a MySQL database.

## Project Structure

The project directory has the following structure:

```
healthCheck/
├── health-monitor-app
│   ├── Dockerfile
│   ├── fetch_result.py
│   ├── healthcheck.py
│   ├── requirements.txt
│   └── templates
│       └── monitor.html
└── mysql
    ├── create_table.sql
    └── Dockerfile

```

## Features
	- Retrieves CPU usage, memory usage, and disk usage information.
	- Stores the system health data in a MySQL database.
	- Presents the system health data in the form of bar graphs.
	- Provides a web interface to view the system health graphs.

##  Requirements
	- Docker

## Usage

1. Clone the repository to your local machine:

```
git clone https://github.com/your-username/health-monitor-app.git
```

2. Navigate to the project directory:

```
cd health-monitor-app
```

3. running following commands step by step

```
	docker network create test
	cd mysql/
	docker build -t mysql_db .
	cd ..
	cd health-monitor-app/
	docker build -t app .
	docker run -d --name mysql-host --network test mysql_db
	docker run -d --name app -p 5000:5000 --network test app
```
 
4. Check the logs

```
	docker logs -f mysql-host
```

5. whenthe mysql-host container is fully up and ready, access at http://localhost:5000/monitor

