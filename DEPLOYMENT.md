````markdown
# 🖥️ Full AWS VM Deployment Guide — FastAPI + Docker + Nginx + HTTPS

This guide will take you from a **fresh AWS EC2 VM** to a **fully HTTPS-enabled FastAPI application** using **Docker**, **Nginx**, and **Certbot**.

---

## ⚙️ Step 0: Launch Your VM

1. Go to **AWS EC2 → Launch Instance**
2. Choose **Ubuntu 22.04 LTS** (or **20.04 LTS**)
3. Pick an instance type — `t2.micro` is fine for small apps
4. Configure **Security Group**:
   - ✅ **SSH (22)** → Your IP
   - ✅ **HTTP (80)** → Anywhere
   - ✅ **HTTPS (443)** → Anywhere
5. Launch and download your **key pair (.pem)**

---

## 🔐 Step 1: SSH Into Your VM

```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@<EC2_PUBLIC_IP>
````

### Update packages

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Git (optional, if you’ll clone the project)

```bash
sudo apt install git -y
```

---

## 🐳 Step 2: Install Docker & Docker Compose

```bash
sudo apt install docker.io docker-compose -y
sudo systemctl enable --now docker
```

### Verify installation

```bash
docker --version
docker-compose --version
```

---

## 🌐 Step 3: Install Nginx

```bash
sudo apt install nginx -y
sudo systemctl enable --now nginx
```

### Check Nginx status

```bash
sudo systemctl status nginx
```

---

## 📦 Step 4: Clone Your FastAPI Project

```bash
cd ~
git clone https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud.git
cd fastapi-async-beyond-crud
```

---

## 🧾 Step 4.1: Create the `.env` File

```bash
sudo nano .env
```

Add your environment variables (example):

```env
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your_secret_key
```

> ⚠️ Make sure the `.env` file is correctly configured **every time** you launch a new VM or pull from GitHub.

---

## 🚀 Step 5: Build & Run Your Docker Containers

### Option 1 — Using Docker Compose (recommended)

```bash
sudo docker compose up -d --build
```

### Option 2 — Single container (no Redis/Celery)

```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
```

Your FastAPI app now runs on **port 8000** inside the VM.

---

## 🌍 Step 6: Configure Nginx as Reverse Proxy

### Create Nginx server block

```bash
sudo nano /etc/nginx/sites-available/fastapi.conf
```

Add the following configuration (replace with your domain):

```nginx
server {
    listen 80;
    server_name kuldeepghorpade-fastapi-beyond-crud.duckdns.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable the configuration

```bash
sudo ln -s /etc/nginx/sites-available/fastapi.conf /etc/nginx/sites-enabled/
```

### Fix long domain issue (Nginx bucket size)

```bash
sudo sed -i '/http {/a \    server_names_hash_bucket_size 128;' /etc/nginx/nginx.conf
```

### Test and reload Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Step 7: Obtain SSL Certificates with Certbot

### Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Run Certbot for your domain

```bash
sudo certbot --nginx -d kuldeepghorpade-fastapi-beyond-crud.duckdns.org
```

Follow the prompts and **choose the redirect HTTP → HTTPS** option.

### Reload Nginx

```bash
sudo systemctl reload nginx
```

Your app is now securely accessible at:
👉 **[https://kuldeepghorpade-fastapi-beyond-crud.duckdns.org](https://kuldeepghorpade-fastapi-beyond-crud.duckdns.org)**

---

## ⚙️ Step 8: Optional Tweaks

### Enable CORS for your frontend

In your FastAPI `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Auto-renew SSL Certificates (Certbot handles automatically)

Test renewal manually:

```bash
sudo certbot renew --dry-run
```

---

## ✅ Summary

| Component     | Purpose                                          |
| ------------- | ------------------------------------------------ |
| **Docker**    | Runs FastAPI + Redis + Celery containers         |
| **Port 8000** | FastAPI internal app port                        |
| **Nginx**     | Reverse proxy handling 80 & 443                  |
| **Certbot**   | Manages free HTTPS certificates                  |
| **DuckDNS**   | Provides free custom domain                      |
| **.env**      | Stores environment variables (must exist per VM) |

---

### 🎉 Your app is now live and production-ready!

FastAPI app → Docker → Nginx → HTTPS (Certbot)
Everything runs securely and automatically renews certificates.

```
