# 🚀 Flask + PostgreSQL + Docker CRUD REST API
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-orange?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.5-blue?logo=docker&logoColor=white)](https://www.docker.com/)

A simple **CRUD REST API** built using **Flask** and **PostgreSQL**, containerized using **Docker**.  
This project demonstrates building, running, and testing backend APIs with database integration.

---

## 📂 Project Structure
| File | Description |
|------|-------------|
| `app.py` | Main Flask application with CRUD endpoints |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Docker configuration for Flask app |
| `.gitignore` | Ignored files for Git |
| `README.md` | This file |

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
git clone https://github.com/<your-username>/Flask-Postgres-CRUD-API.git
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
docker build -t postgres:15 .
docker run -d --name my_postgres --network mynetwork -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=cruddb -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:15
```
### 6️⃣ check live logs
```bash
docker logs my-python-container -f
docker logs my-postgres -f
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
### Test APIs using Postman / Curl
Flask app run http://localhost:5000
**Add Student (POST)**
```bash
POST http://localhost:5000/students
Body (JSON):
{
  "firstname": "Samarth",
  "lastname": "Garde",
  "birthdate": "2002-05-14",
  "email": "samarth@example.com",
  "enrolled_date": "2025-09-25"
}
```
**Get All Students (GET)**
```bash
GET http://localhost:5000/students
```
**Get Student by ID (GET)**
```bash
GET http://localhost:5000/students/1
```
**Update Item (PUT)**
PUT http://localhost:5000/items/1
Body (JSON):
```bash
{
  "name": "New Item Name",
  "description": "Updated Description"
}
```
**Delete Item (DELETE)**
```bash
DELETE http://localhost:5000/items/1
```
### 9 Direct DB Check
```bash
docker exec -it my_postgres psql -U postgres -d cruddb
SELECT * FROM students;
SELECT * FROM items;
```

