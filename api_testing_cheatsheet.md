# 🚀 FastAPI Beyond CRUD — API Testing Cheat Sheet

> **Base URL (Local):** `http://localhost:8000`  
> **Auth:** All protected endpoints need `Bearer Token` in Postman → Authorization tab → Bearer Token  
> **Start Server:** `docker compose up -d` (starts FastAPI + Redis + Celery together)

---

## 🟢 PHASE 1: System Endpoints (No Token Needed)

| # | Method | URL | Expected |
|---|--------|-----|----------|
| 1 | `GET` | `/` | `200 OK` — Welcome message + version |
| 2 | `GET` | `/health` | `200 OK` — `{"status": "healthy"}` |

---

## 🔐 PHASE 2: Authentication Flow (No Token Needed)

### Step 1 — Sign Up
```
POST /api/v1/auth/signup
Body:
{
  "first_name": "kuldeep",
  "last_name": "ghorpade",
  "username": "kuldeepghorpade",
  "email": "kuldeepghorpade10@gmail.com",
  "password": "123456"
}
✅ Response: 201 Created — user object + verification_link
```

### Step 2 — Verify Email
```
GET /api/v1/auth/verify/<token-from-verification_link>
⚠️  Replace domain with localhost:8000 in the link!
✅ Response: 200 OK — "Account verified successfully"
```

### Step 3 — Login (Get Token)
```
POST /api/v1/auth/login
Body:
{
  "email": "kuldeepghorpade10@gmail.com",
  "password": "123456"
}
✅ Response: 200 OK — access_token + refresh_token
📌 Copy access_token — needed for ALL protected endpoints!
```

### Step 4 — Password Reset (2-step flow)
```
Step A: POST /api/v1/auth/password-reset-request
Body: { "email": "kuldeepghorpade10@gmail.com" }
✅ Response: reset_link in JSON (replace domain with localhost:8000)

Step B: POST /api/v1/auth/password-reset-confirm/<token>
Body:
{
  "new_password": "MyNewPassword789!",
  "confirm_new_password": "MyNewPassword789!"
}
✅ Response: "Password reset successfully"
```

---

## 📚 PHASE 3: Books Module (Bearer Token Required)

> All requests need: Authorization → Bearer Token → paste access_token

| # | Method | URL | Body | Expected |
|---|--------|-----|------|----------|
| 1 | `POST` | `/api/v1/books/` | Book JSON below | `201 Created` |
| 2 | `GET` | `/api/v1/books/` | None | `200 OK` — list of books |
| 3 | `GET` | `/api/v1/books/<book_uid>` | None | `200 OK` — single book with tags & reviews |
| 4 | `GET` | `/api/v1/books/user/<user_uid>` | None | `200 OK` — books by that user |
| 5 | `PATCH` | `/api/v1/books/<book_uid>` | `{"title": "Updated Title"}` | `200 OK` |
| 6 | `DELETE` | `/api/v1/books/<book_uid>` | None | `204 No Content` |

**Create Book Body:**
```json
{
  "title": "Mastering FastAPI Async",
  "author": "Kuldeep Ghorpade",
  "publisher": "Tech Press",
  "published_date": "2024-01-01",
  "page_count": 300,
  "language": "English"
}
```
> 📌 After creating, **copy the `uid`** from the response — needed for Reviews & Tags!

---

## ⭐ PHASE 4: Reviews Module (Bearer Token Required)

| # | Method | URL | Note |
|---|--------|-----|------|
| 1 | `POST` | `/api/v1/reviews/book/<book_uid>` | Add a review to a specific book |
| 2 | `GET` | `/api/v1/reviews/<review_uid>` | Get a specific review |
| 3 | `DELETE` | `/api/v1/reviews/<review_uid>` | Delete your own review |
| 4 | `GET` | `/api/v1/reviews/` | **Admin only** — regular user gets `401` |

**Add Review Body:**
```json
{
  "rating": 4,
  "review_text": "This book completely changed how I think about APIs!"
}
```

> 🔐 **RBAC Demo:** Hit `GET /api/v1/reviews/` with a user token → `401 Unauthorized`.  
> Switch to admin token → `200 OK` with all reviews. This proves Role-Based Access Control works!

---

## 🏷️ PHASE 5: Tags Module (Bearer Token Required)

| # | Method | URL | Body | Expected |
|---|--------|-----|------|----------|
| 1 | `POST` | `/api/v1/tags/` | `{"name": "Backend Development"}` | `201 Created` |
| 2 | `GET` | `/api/v1/tags/` | None | `200 OK` — list of all tags |
| 3 | `POST` | `/api/v1/tags/book/<book_uid>/tags` | TagAddModel below | `200 OK` — book with tags nested |
| 4 | `PUT` | `/api/v1/tags/<tag_uid>` | `{"name": "FastAPI & Python"}` | `200 OK` — updated tag |
| 5 | `DELETE` | `/api/v1/tags/<tag_uid>` | None | `204 No Content` |

**Attach Tag to Book Body:**
```json
{
  "tags": [
    { "name": "Backend Development" }
  ]
}
```
> ⚠️ Note: Tags are attached by **name**, not by uid. If the tag name doesn't exist, it gets auto-created.

**Verify Tag is Attached:**
```
GET /api/v1/books/<book_uid>
→ Response will contain "tags": [...] array with attached tags inside the book JSON
```

---

1. **Async Background Tasks:** Signup triggers a Celery task to send a verification email via Redis — the API responds instantly without waiting for the email to send.
2. **JWT Security:** Login returns both a short-lived `access_token` and a long-lived `refresh_token` — industry standard pattern.
3. **RBAC:** `GET /reviews/` is admin-only. Regular users are blocked with `401`. Admins see everything. Enforced automatically by the `RoleChecker` dependency.
4. **Docker Architecture:** 3 containers working together — FastAPI app, Redis broker, Celery worker — all on a shared Docker network.
5. **Secure Tokens:** Email verification & password reset use `itsdangerous` to generate cryptographically signed, expiring URL tokens.
6. **Production Deployment:** Nginx reverse proxy + Certbot SSL + AWS EC2 + DuckDNS domain — fully production-ready.
