# 🚀 FastAPI Async Beyond CRUD

This is a modernized and asynchronous version of the **FastAPI Beyond CRUD** project.  
It demonstrates advanced backend development concepts in **FastAPI**, including authentication, background tasks with Celery, async database handling, and more — going far beyond basic CRUD operations.

---

## 📚 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)
5. [Running the Application](#running-the-application)
6. [Running Tests](#running-tests)
7. [Project Structure](#project-structure)
8. [Contributing](#contributing)

---

## 🧩 Overview

This project focuses on **async FastAPI development** with production-ready architecture:
- Uses **SQLModel** with **Alembic** migrations.
- Supports **JWT authentication**.
- Integrates **Celery + Redis** for background tasks (like sending emails).
- Uses **Neon PostgreSQL** as a managed database.
- Includes email verification and scalable Docker setup.

---

## ✨ Features
- 🔐 JWT Authentication (Access & Refresh tokens)
- 📧 Email Verification with Celery
- 📚 Async SQLModel + Alembic migrations
- 🐘 PostgreSQL (Neon Cloud)
- 🐳 Docker support for production
- 🧪 Unit testing with Pytest

---

## ⚙️ Tech Stack
- **FastAPI** — Async Python web framework  
- **SQLModel** — ORM based on SQLAlchemy  
- **Alembic** — Database migrations  
- **Celery** — Background task queue  
- **Redis** — Message broker for Celery  
- **PostgreSQL (Neon)** — Cloud database  
- **Docker** — Containerized deployment  

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud.git
cd fastapi-async-beyond-crud
````

### 2️⃣ Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

### 5️⃣ Apply database migrations

```bash
alembic upgrade head
```

### 6️⃣ Start Celery worker (for email/background tasks)

```bash
sh runworker.sh
```

---

## 🧠 Running the Application

### Run locally (development)

```bash
fastapi dev src/
```

### Or using Uvicorn

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Or with Docker

```bash
docker compose up -d
```

---

## 🧪 Running Tests

Run all test cases:

```bash
pytest
```

---

## 🗂️ Project Structure

```
fastapi-async-beyond-crud/
│
├── alembic.ini
├── compose.yml
├── requirements.txt
├── runworker.sh
├── Dockerfile
├── .env.example
│
├── src/
│   ├── auth/              # Authentication and JWT logic
│   ├── db/                # Database models and connection
│   ├── mail/              # Email templates and Celery tasks
│   ├── routes/            # API endpoints
│   ├── core/              # Config and constants
│   └── main.py            # App entry point
│
└── migrations/            # Alembic migration files
```

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!

Fork the repo and create a PR:
👉 [https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud](https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud)

---

### ⭐ If you find this project helpful, give it a star on GitHub!


