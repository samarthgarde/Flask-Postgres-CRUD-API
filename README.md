# 🚀 Flask + PostgreSQL + Docker CRUD REST API
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-orange?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.5-blue?logo=docker&logoColor=white)](https://www.docker.com/)

A simple **CRUD REST API** built using **Flask** and **PostgreSQL**, containerized using **Docker**.  
This project demonstrates building, running, and testing backend APIs with database integration.

---

## 📂 Project Structure
```bash
flask-postgres-crud/
├── Dockerfile # Dockerfile to containerize the Flask app
├── app.py # Main Flask application
├── database/ # PostgreSQL database setup scripts
|     └── Dockerfile  # Dockerfile to the containerizeto postgresql
├── requirements.txt # Python dependencies
├── venv/ # Python virtual environment
└── README.md
```
---

## ⚡ Features
- Create, Read, Update, Delete (CRUD) operations  
- RESTful API design  
- PostgreSQL database integration  
- Docker containerized (easy deployment)  

---

## 🛠 Tech Stack
- **Backend:** Python 3.11, Flask 2.3.2  
- **Database:** PostgreSQL 15  
- **Containerization:** Docker  
- **ORM:** SQLAlchemy  

---

## 📦 Setup & Run

### 1️⃣ Clone Repo
```bash
git clone https://github.com/samarthgarde/Flask-Postgres-CRUD-API.git
cd Flask-Postgres-CRUD-API
```
### 2️⃣ virtual environment set and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```
### 2️⃣ Create network
```bash
docker network create mynetwork
```
### 3️⃣ Create volume
```bash
docker volume create pgdata
```
### 4️⃣ Build & Run my-webapp container
```bash
docker build -t flask-app .
docker run -d --name my-python-container --network mynetwork -e DATABASE_URL=postgresql://postgres:postgres@my_postgres:5432/cruddb -p 5000:5000 flask-app
```
### 5️⃣ Build & Run postgres:15 container
```bash
cd database/
docker build -t postgres:15 .
docker run -d --name my_postgres --network mynetwork -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=cruddb -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:15
```
### 6️⃣ check live logs
```bash
docker logs my-postgres -f
docker logs my-python-container -f
```
### 7 Network Check
```bash
docker network ls
docker network inspect mynetwork
```
### 8 Environment Variable Check (DATABASE_URL)
```bash
docker exec -it my-python-container env | grep DATABASE_URL
```
### Test APIs using Postman / Curl / Browser (for GET requests)

**Test "Get all students" (GET)**
- **URL**:http://localhost:5001/students
- **Method**: GET
```bash
curl http://localhost:5001/students
```
---

**Test "Add student" (POST)**
**URL**: http://localhost:5001/students
**Method**: POST
**Body (JSON)**:
```bash
{
  "firstname": "samarth",
  "lastname": "garde",
  "birthdate": "2000-01-01",
  "email": "samarthgarde@example.com",
  "enrolled_date": "2025-09-30"
}
```
- Using curl:
```bash
curl -X POST http://localhost:5001/students \
-H "Content-Type: application/json" \
-d '{"firstname":"samarth",garde":"Doe","birthdate":"2000-01-01","email":"samarthgarde@example.com","enrolled_date":"2025-09-30"}'
```
----

**Test "Get single student" (GET)**
**URL:** http://localhost:5001/students/1

**Method:** GET
```bash
curl http://localhost:5001/students/1
```
---

**Test "Add item" (POST)**
**URL:** http://localhost:5001/items
**Body (JSON):**
```bash
{
  "name": "Book",
  "description": "Python Programming Book"
}
```
- usage with curl:
```bash
curl -X POST http://localhost:5001/items \
-H "Content-Type: application/json" \
-d '{"name":"Laptop","description":"Gaming laptop"}'
```
- **Get all items**
```bash
curl http://localhost:5001/items/1
```
- **Update an item**
```bash
{"id":1,"name":"Laptop Pro","description":"High-end gaming laptop"}
```
- **Delete an item**
```bash
curl -X DELETE http://localhost:5001/items/1
```

### 9 Using psql in terminal (Postgres CLI)
**Step 1: Access Postgres container**
```bash
docker exec -it my_postgres psql -U postgres -d cruddb
```
**Step 2: Show tables**
```bash
\dt
```
**Step 3: Select data in a table format**
```bash
SELECT * FROM students;
SELECT * FROM items;
```
- To exit psql
```bash
\q
```
----

### Using a GUI tool
- **pgAdmin** (official, free)
**Steps:**
**1.Add a new server**
- Right-click Servers → Create → Server…
- General tab:
- Name: MyDockerPostgres (any name)
- Connection tab:
- Host name/address: localhost
- Port: 5432
- Username: postgres
- Password: postgres
**2.Save Password: check the box**
**Click Save.**
  
**3.Verify connection**
- Expand Servers → **MyDockerPostgres** → **Databases** → **cruddb**→ **Schemas** → **public** → **Tables**
- You should see your tables: students and items.

**View data in table format**
Right-click table (e.g., students) → View/Edit Data → All Rows
pgAdmin shows data in a spreadsheet-like format.
You can edit, delete, or insert rows directly in pgAdmin.
Also, you can run custom SQL queries in Query Tool (Tools → Query Tool)
```bash
SELECT * FROM students;
SELECT * FROM items;
```
