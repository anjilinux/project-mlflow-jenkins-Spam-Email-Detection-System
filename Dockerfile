FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app

# System deps
RUN apt update && apt install -y \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
