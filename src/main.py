from fastapi import FastAPI
from src.auth.routes import auth_router
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router

app = FastAPI(
    title="FastAPI Beyond CRUD - Open Source by Kuldeep Ghorpade",
    description=(
        "📘 A production-ready FastAPI project featuring modular architecture, "
        "authentication, books, reviews, and tags modules.\n\n"
        "FastAPI Async Beyond CRUD - A production-ready, asynchronous FastAPI backend. Fully containerized with Docker & Docker Compose, secured with Nginx + Certbot (HTTPS). Uses Redis + Celery for background tasks, SQLAlchemy + Alembic for ORM and migrations, Neon PostgreSQL as the production database, with JWT auth, AWS EC2 hosting, and DuckDNS domain \n\n"
        "🔗 GitHub Repository: https://github.com/kuldeepghorpade05/fastapi-async-beyond-crud.git \n\n"
        "Maintainer: Kuldeep Ghorpade"

    ),
    version="1.0.0",
)


# Include routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(book_router, prefix="/api/v1/books")
app.include_router(review_router, prefix="/api/v1/reviews")
app.include_router(tags_router, prefix="/api/v1/tags")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": (
            "Hello from Kuldeep Ghorpade, "
            "Service running successfully! - FastAPI Beyond CRUD"
        ),
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "auth": "/api/v1/auth",
            "books": "/api/v1/books",
            "reviews": "/api/v1/reviews",
            "tags": "/api/v1/tags"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
