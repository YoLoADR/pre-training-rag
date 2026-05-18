FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour pymupdf et faiss
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY homebutler/ ./homebutler/
COPY api/ ./api/
COPY data/ ./data/

ENV LLM_PROVIDER=ollama
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
