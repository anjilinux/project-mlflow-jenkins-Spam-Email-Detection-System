FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app

# System deps
RUN apt update && apt install -y python3 python3-pip

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# 🔥 REQUIRED: keep container alive
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]

