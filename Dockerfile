# 1️⃣ Use official Python image
FROM python:3.13-slim

# 2️⃣ Set working directory inside the container
WORKDIR /app

# 3️⃣ Install Poetry
RUN pip install --no-cache-dir poetry

# 4️⃣ Copy dependency files first (for caching)
COPY pyproject.toml poetry.lock* ./

# 5️⃣ Install dependencies using Poetry (fixed for v1.5+)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# 6️⃣ Copy project source code
COPY ./src ./src

# 7️⃣ Default command to run FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
