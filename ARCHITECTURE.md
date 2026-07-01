# 🏗️ System Architecture & Technical Design

## Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Data Flow Diagrams](#data-flow-diagrams)
- [Technology Stack Details](#technology-stack-details)
- [Communication Protocols](#communication-protocols)
- [Database Schema](#database-schema)
- [AI/ML Pipeline](#aiml-pipeline)

---

## System Overview

**Safety Road** is a **mobile-first, AI-powered application** that follows a **client-server architecture** with edge processing capabilities.

### Key Principles

- **Real-time Detection** - Instant pothole identification via camera
- **Scalable Backend** - FastAPI for high-concurrency inference
- **Privacy-First** - Local data storage with optional cloud sync
- **Mobile Optimized** - YOLOv8 Nano for efficient processing
- **User-Centric** - Interactive map with actionable insights

---

## Component Architecture

### 1. Frontend Architecture (React Native/Expo)

```
┌─────────────────────────────────────────────────────┐
│           React Native Mobile Application           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │         React Navigation Layer               │   │
│  │  • Tab Navigator (Home, Map, Reports)        │   │
│  │  • Stack Navigator (Modal flows)             │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │       Screen Components (TypeScript)        │   │
│  │  • index.tsx (Detection Screen)              │   │
│  │  • explore.tsx (Map Screen)                  │   │
│  │  • report.tsx (Report Screen)                │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │     Service Layer (Business Logic)          │   │
│  │  • api.ts (HTTP requests)                    │   │
│  │  • potholeDetection.ts (Detection logic)     │   │
│  │  • storage.ts (Local persistence)            │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │      Native APIs & Libraries                │   │
│  │  • Expo Camera (Image capture)               │   │
│  │  • Expo Location (GPS coordinates)           │   │
│  │  • Expo MediaLibrary (Gallery access)        │   │
│  │  • Mapbox GL (Map rendering)                 │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │      Local Storage Layer (AsyncStorage)     │   │
│  │  • Detected potholes data                    │   │
│  │  • User preferences                          │   │
│  │  • Cache data                                │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2. Backend Architecture (FastAPI/Python)

```
┌─────────────────────────────────────────────────────┐
│         FastAPI Backend Application                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │      API Layer (FastAPI Routes)             │   │
│  │  • POST /detect - Image detection           │   │
│  │  • GET /health - System status              │   │
│  │  • POST /batch - Batch processing           │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │    Request Processing Layer                 │   │
│  │  • Input validation (Pydantic)              │   │
│  │  • Image decoding (base64)                  │   │
│  │  • GPS coordinate handling                  │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │    Image Processing Pipeline                │   │
│  │  • Image resizing (640x640)                 │   │
│  │  • Normalization                            │   │
│  │  • Format conversion                        │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │    YOLOv8 Inference Engine                  │   │
│  │  • Model loading                            │   │
│  │  • Real-time detection                      │   │
│  │  • Bounding box generation                  │   │
│  │  • Confidence score calculation             │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │    Post-Processing Layer                    │   │
│  │  • Severity classification                  │   │
│  │  • Result formatting                        │   │
│  │  • GPS coordinate integration               │   │
│  └─────────────────────────────────────────────┘   │
│           ⬇                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │    Response Formatting & Caching            │   │
│  │  • JSON response creation                   │   │
│  │  • Performance metrics                      │   │
│  │  • Error handling                           │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Flow 1: Image Detection Workflow

```
┌─────────────────┐
│  User captures  │
│  pothole image  │
│  via camera     │
└────────┬────────┘
         │
         ⬇
┌─────────────────────────────────────┐
│  Encode image to base64             │
│  Attach GPS coordinates             │
│  Create detection request           │
└────────┬────────────────────────────┘
         │
         ⬇
    ┌─────────────┐
    │ HTTP POST   │ ━━━━━━━━━━━━━━━━━┐
    │ /detect     │                  │
    └─────────────┘                  │
         ⬅━━━━━━━━━━━━━━━━━━━━━━━━━━┫
         │                            │
         │          ┌────────────────────────────────────────┐
         │          │    Backend Processing                  │
         │          │                                        │
         │          │ 1. Decode base64 image                │
         │          │ 2. Validate input data                │
         │          │ 3. Preprocess image (640x640)         │
         │          │ 4. Run YOLOv8 model inference         │
         │          │ 5. Extract bounding boxes             │
         │          │ 6. Calculate confidence scores        │
         │          │ 7. Classify severity level            │
         │          │ 8. Format response JSON               │
         │          │                                        │
         │          └────────────────────────────────────────┘
         │
         ⬇
┌──────────────────────────────────────┐
│ Receive detection results:           │
│ • Pothole locations (bbox)           │
│ • Confidence scores                  │
│ • Severity classification            │
│ • Processing time                    │
└────────┬─────────────────────────────┘
         │
         ⬇
┌──────────────────────────────────────┐
│ Store in local SQLite DB:            │
│ • Detection timestamp                │
│ • GPS coordinates                    │
│ • Image reference                    │
│ • Severity level                     │
└────────┬─────────────────────────────┘
         │
         ⬇
┌──────────────────────────────────────┐
│ Display on map:                      │
│ • Add marker at GPS location         │
│ • Color code by severity             │
│ • Show detection details             │
│ • Update statistics                  │
└──────────────────────────────────────┘
```

---

## Technology Stack Details

### Frontend Stack

#### React Native + Expo

- **Why**: Cross-platform (iOS/Android) with single codebase
- **Benefits**: Faster development, immediate testing
- **Version**: Latest stable (50.x+)

#### TypeScript

- **Why**: Type safety for complex app logic
- **Benefits**: Fewer runtime errors, better IDE support
- **Usage**: All components, services, and utilities

#### State Management

- **Approach**: React Context + useState hooks
- **Storage**: AsyncStorage for persistence

### Backend Stack

#### FastAPI

- **Why**: Modern Python framework, auto-documentation
- **Features**: Automatic API docs, dependency injection, CORS handling

#### YOLOv8 (Ultralytics)

- **Model**: YOLOv8 Nano (smallest variant)
- **Advantages**: Real-time detection, low memory, high accuracy

#### Model Specifications

```
Model: YOLOv8 Nano
Parameters: ~3.1M
File Size: ~6.3MB
Input: 640x640 RGB images
Speed: ~50-100ms inference
```

---

## Communication Protocols

### REST API Specification

#### Detection Endpoint

```
POST /detect
Content-Type: application/json
```

---

## Database Schema

### SQLite Local Storage

#### Potholes Table

```sql
CREATE TABLE potholes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  severity TEXT NOT NULL,
  confidence REAL NOT NULL,
  detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  image_path TEXT,
  UNIQUE(latitude, longitude, detected_at)
);
```

---

## AI/ML Pipeline

### Training Pipeline

```
Step 1: Dataset Preparation
Step 2: Model Training
Step 3: Model Evaluation
Step 4: Model Optimization
Step 5: Deployment
```

### Severity Classification Logic

```
IF confidence >= 0.80: severity = "HIGH"
ELIF confidence >= 0.50: severity = "MEDIUM"
ELSE: severity = "LOW"
```

---

This architecture ensures **scalability, reliability, and maintainability**.
