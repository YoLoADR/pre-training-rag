FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit==1.41.1 plotly==5.24.1 requests==2.32.3 pandas==2.2.3

COPY ui/ ./ui/
COPY homebutler/ ./homebutler/

ENV API_URL=http://api:8000

EXPOSE 8501

CMD ["streamlit", "run", "ui/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
