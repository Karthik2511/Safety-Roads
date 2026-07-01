# 📡 Backend API Documentation

Complete REST API reference for the pothole detection backend.

## Base URL

```
http://localhost:8000
```

## API Overview

| Endpoint  | Method | Purpose                           |
| --------- | ------ | --------------------------------- |
| `/health` | GET    | System health check               |
| `/detect` | POST   | Detect potholes in image          |
| `/batch`  | POST   | Batch image processing            |
| `/docs`   | GET    | Auto-generated API docs (Swagger) |

---

## Endpoints

### 1. Health Check

**Get backend system status**

```
GET /health
```

#### Response

```json
{
  "status": "operational",
  "model_loaded": true,
  "model_version": "yolov8n",
  "uptime_seconds": 3600,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Example Request

```bash
curl -X GET http://localhost:8000/health
```

---

### 2. Image Detection

**Detect potholes in a single image**

```
POST /detect
Content-Type: application/json
```

#### Request Body

```json
{
  "image": "base64_encoded_image_string",
  "lat": 12.9716,
  "lon": 77.5946,
  "timestamp": "2024-01-15T10:30:00Z",
  "confidence_threshold": 0.5
}
```

#### Request Parameters

| Parameter              | Type   | Required | Description                        |
| ---------------------- | ------ | -------- | ---------------------------------- |
| `image`                | string | ✅       | Base64 encoded image (JPEG/PNG)    |
| `lat`                  | float  | ✅       | Latitude (-90 to 90)               |
| `lon`                  | float  | ✅       | Longitude (-180 to 180)            |
| `timestamp`            | string | ❌       | ISO 8601 timestamp                 |
| `confidence_threshold` | float  | ❌       | Detection threshold (default: 0.5) |

#### Response

```json
{
  "success": true,
  "detections": [
    {
      "id": "det_001",
      "class": "pothole",
      "confidence": 0.92,
      "severity": "high",
      "bbox": {
        "x": 150,
        "y": 200,
        "width": 100,
        "height": 80
      }
    }
  ],
  "summary": {
    "total_detections": 1,
    "severity_count": {
      "high": 1,
      "medium": 0,
      "low": 0
    }
  },
  "processing": {
    "inference_time_ms": 87,
    "total_time_ms": 99
  },
  "gps_data": {
    "lat": 12.9716,
    "lon": 77.5946,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

#### Status Codes

- `200 OK` - Detection successful
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Processing error

#### Example Python

```python
import requests
import base64

# Read and encode image
with open("pothole.jpg", "rb") as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

# Send request
response = requests.post(
    "http://localhost:8000/detect",
    json={
        "image": image_base64,
        "lat": 12.9716,
        "lon": 77.5946
    }
)

# Process response
results = response.json()
print(f"Detections: {results['summary']['total_detections']}")
```

---

### 3. Batch Processing

**Process multiple images in a batch**

```
POST /batch
Content-Type: application/json
```

#### Request Body

```json
{
  "images": [
    {
      "data": "base64_encoded_image_1",
      "lat": 12.9716,
      "lon": 77.5946,
      "id": "img_001"
    },
    {
      "data": "base64_encoded_image_2",
      "lat": 12.9717,
      "lon": 77.5947,
      "id": "img_002"
    }
  ],
  "parallel": true
}
```

#### Response

```json
{
  "success": true,
  "batch_id": "batch_abc123",
  "total_images": 2,
  "results": [
    {
      "image_id": "img_001",
      "status": "success",
      "detections": [...]
    }
  ]
}
```

---

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INVALID_IMAGE",
    "message": "Image must be JPEG or PNG format"
  },
  "request_id": "req_xyz123"
}
```

### Common Error Codes

| Code                  | Status | Description                      |
| --------------------- | ------ | -------------------------------- |
| `INVALID_IMAGE`       | 400    | Invalid image format or encoding |
| `IMAGE_TOO_LARGE`     | 413    | Image exceeds size limit (5MB)   |
| `INVALID_COORDINATES` | 400    | GPS coordinates out of range     |
| `MODEL_NOT_LOADED`    | 503    | YOLOv8 model not initialized     |
| `PROCESSING_ERROR`    | 500    | Error during inference           |

---

## Interactive API Documentation

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc

```
http://localhost:8000/redoc
```

---

## Performance Benchmarks

| Metric         | Typical  | Range        |
| -------------- | -------- | ------------ |
| Preprocessing  | 10ms     | 5-20ms       |
| Inference      | 75ms     | 50-150ms     |
| Postprocessing | 5ms      | 2-10ms       |
| **Total**      | **90ms** | **60-180ms** |

---

**Last Updated**: January 2024
**Version**: 1.0
