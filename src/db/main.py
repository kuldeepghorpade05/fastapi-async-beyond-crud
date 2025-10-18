# src/db/main.py

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.config import Config
from typing import AsyncGenerator

# ✅ Improved async engine for Neon PostgreSQL
async_engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,  # logs SQL statements
    connect_args={"ssl": True},
    pool_pre_ping=True,      # ✅ tests connection before using it
    pool_recycle=1800,       # ✅ recycles every 30 mins
    pool_size=5,             # ✅ small pool for async apps
    max_overflow=10          # ✅ allows extra connections when needed
)

# Async session factory
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize DB tables
async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency for FastAPI routes
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
