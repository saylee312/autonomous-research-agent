# Multi-stage build: build frontend then build python runtime
FROM node:22-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

RUN npm run build

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install common system dependencies required by data-processing packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential git curl libgl1 libsm6 libxrender1 libxext6 \
       tesseract-ocr poppler-utils pkg-config libjpeg-dev libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch==2.3.1 \
    torchvision==0.18.1 \
    --index-url https://download.pytorch.org/whl/cpu

# Install the remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy backend source
COPY backend ./backend

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist ./frontend_dist

EXPOSE 8000
ENV PORT=8000
CMD ["sh","-c","uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
