from fastapi import FastAPI
from src.auth.routes import auth_router
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router

app = FastAPI(title="FastAPI Beyond CRUD")

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(book_router, prefix="/api/v1/books")
app.include_router(review_router, prefix="/api/v1/reviews")
app.include_router(tags_router, prefix="/api/v1/tags")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI Beyond CRUD is running!"}
