# 🚀 FastAPI Async Beyond CRUD

A **production-ready, asynchronous FastAPI backend**, deployed on **AWS EC2** using **Docker Compose**, secured via **Nginx + Certbot**, and running under a **DuckDNS** domain.

This project goes **beyond CRUD**, implementing real-world backend features such as **JWT authentication**, **async database operations**, and **email verification using Celery and Redis**.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)
5. [Running the Application](#running-the-application)
6. [Docker Deployment](#docker-deployment)
7. [Nginx + HTTPS Setup](#nginx--https-setup)
8. [Project Structure](#project-structure)
9. [Contributing](#contributing)

---

## 🧩 Overview

This version of **FastAPI Async Beyond CRUD** is optimized for **production environments** and demonstrates modern **asynchronous backend development** best practices.

* 🐳 Fully containerized using **Docker + Docker Compose**
* 🔒 Secured with **Nginx + Certbot (HTTPS)**
* ⚙️ **Redis + Celery** for background task handling (email verification)
* 🧱 **SQLAlchemy + Alembic** for ORM and database migrations
* 🐘 **Neon PostgreSQL** as the production database
* 📦 **Poetry** for dependency management
* ☁️ Hosted on **AWS EC2**
* 🌐 Domain handled by **DuckDNS**
* 🧪 **Postman** and **Swagger UI** used for API testing — Swagger comes auto-configured with **FastAPI**

---

## ✨ Features

* 🔐 **JWT Authentication** (Access & Refresh Tokens)
* 📧 **Email Verification** with **Celery + Redis**
* ⚡ **Async SQLAlchemy ORM** and **Alembic Migrations**
* 🐘 **PostgreSQL (Neon Cloud)** for scalable database hosting
* 🐳 **Docker Compose** setup for FastAPI, Redis, and Celery containers
* 🌐 **Nginx + Certbot** for secure HTTPS deployment
* ☁️ **AWS EC2** hosting with **DuckDNS** domain support
* 🧰 **Poetry** for dependency and environment management
* 🧪 **Postman + Swagger UI** for API testing and documentation

---

## ⚙️ Tech Stack

| Category               | Technologies            |
| ---------------------- | ----------------------- |
| **Framework**          | FastAPI (Async)         |
| **ORM + Migrations**   | SQLAlchemy + Alembic    |
| **Task Queue**         | Celery                  |
| **Message Broker**     | Redis                   |
| **Database**           | PostgreSQL (Neon Cloud) |
| **Web Server + SSL**   | Nginx + Certbot         |
| **Containerization**   | Docker + Docker Compose |
| **Dependency Manager** | Poetry                  |
| **Hosting**            | AWS EC2                 |
| **Domain**             | DuckDNS                 |
| **API Testing**        | Swagger UI + Postman    |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud.git
cd fastapi-async-beyond-crud
```

### 2️⃣ (Optional) Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies Using Poetry

```bash
poetry install
```

### 4️⃣ Configure Environment Variables

```bash
cp .env.example .env
```

Fill in your configuration values:

* `DATABASE_URL` → Neon PostgreSQL connection string
* `REDIS_URL` → Redis connection URL
* `SECRET_KEY` → JWT secret key
* `MAIL_USERNAME`, `MAIL_PASSWORD`, etc.

### 5️⃣ Apply Database Migrations

```bash
alembic upgrade head
```

### 6️⃣ Start Celery Worker for Background Tasks

```bash
sh runworker.sh
```

Celery handles:

* Sending verification emails
* Running asynchronous background tasks

---

## 🧠 Running the Application (Local)

### Using FastAPI Dev Mode

```bash
fastapi dev src/
```

### Or with Uvicorn

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI auto-configured by FastAPI)

---

## 🐳 Docker Deployment

### Build and Run Containers

```bash
docker compose up -d --build
```

This starts:

* 🧩 **FastAPI container** (backend app)
* 🔁 **Redis container** (message broker)
* ⚙️ **Celery container** (background worker)
* 🌐 **Nginx container** (reverse proxy + HTTPS via Certbot)

Check running containers:

```bash
docker ps
```

Stop all services:

```bash
docker compose down
```

---

## 🔒 Nginx + HTTPS Setup

The application runs securely through **Nginx**, with **Certbot** managing SSL certificates for your **DuckDNS** domain.

### Key Highlights

1. **Nginx** forwards all traffic from ports `80/443` → FastAPI container (`8000`)
2. **Certbot** automatically issues and renews SSL certificates
3. **HTTP → HTTPS** redirection is enforced globally
4. **Certificates auto-renew** via Cron/systemd timers

Access your application at:
🌐 `https://<your-domain>.duckdns.org`

---

## 🗂️ Project Structure

```
fastapi-async-beyond-crud/
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── migrations/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 11d1f79aef4d_add_users.py
│       ├── a04d79012711_add_tags_table.py
│       ├── dba4f311e944_add_review_table.py
│       └── __pycache__/
│
├── notes.txt
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── runworker.sh
├── README.md
│
└── src/
    ├── auth/
    │   ├── dependencies.py
    │   ├── routes.py
    │   ├── schemas.py
    │   ├── service.py
    │   └── utils.py
    │
    ├── books/
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    │
    ├── reviews/
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    │
    ├── tags/
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    │
    ├── db/
    │   ├── main.py
    │   ├── models.py
    │   └── redis.py
    │
    ├── celery_tasks.py
    ├── config.py
    ├── errors.py
    ├── mail.py
    ├── main.py
    ├── middleware.py
    └── __init__.py
```

---

## 🤝 Contributing

Contributions and improvements are always welcome!

Fork the repository and create a PR here:
👉 [https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud](https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud)

---

### ⭐ If you found this project helpful, please consider giving it a **star** on GitHub!

