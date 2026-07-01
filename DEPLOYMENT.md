# 🚀 Deployment Guide - Safety Road

Production deployment instructions for AWS, Azure, GCP, and Docker.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Azure Deployment](#azure-deployment)
- [GCP Deployment](#gcp-deployment)

---

## Quick Start

### Docker Compose (Local)

```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/yolov8n.pt
      - API_HOST=0.0.0.0
      - API_PORT=8000
```

Deploy:

```bash
docker-compose up -d
```

---

## Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & Run:

```bash
docker build -t pothole-detector:latest .
docker run -p 8000:8000 pothole-detector:latest
```

---

## AWS Deployment

### Option 1: AWS Lambda + API Gateway

```bash
npm install -g serverless
serverless deploy
```

### Option 2: AWS ECS + Fargate

```bash
# Push image to ECR
docker push YOUR_ECR_URI/pothole-detector:latest

# Create ECS service
aws ecs create-service \
  --cluster pothole-detector \
  --service-name pothole-api \
  --task-definition pothole-detector:1
```

---

## Azure Deployment

### Azure Container Instances

```bash
az container create \
  --resource-group pothole-detector \
  --name pothole-detector \
  --image potholdetector.azurecr.io/api:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000
```

### Azure App Service

```bash
az webapp create \
  --resource-group pothole-detector \
  --plan pothole-plan \
  --name pothole-detector-api \
  --runtime "PYTHON:3.11"
```

---

## GCP Deployment

### Google Cloud Run

```bash
gcloud run deploy pothole-detector \
  --image gcr.io/PROJECT_ID/pothole-detector \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2
```

---

## Monitoring

All cloud providers offer built-in monitoring:

- **AWS**: CloudWatch
- **Azure**: Application Insights
- **GCP**: Cloud Trace

---

## Security

### Environment Variables

```env
API_DEBUG=False
API_WORKERS=4
CORS_ORIGINS=["https://yourdomain.com"]
LOG_LEVEL=INFO
```

### SSL/TLS

Use Let's Encrypt for HTTPS certificates.

---

**Ready for production!** 🚀
