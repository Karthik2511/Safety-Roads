# 🚀 Complete Setup Guide - Safety Road

Complete installation, configuration, and deployment instructions for the pothole detection system.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)

---

## Prerequisites

### System Requirements

- **Windows 10/11, macOS, or Linux**
- **Node.js 16+** and npm 8+
- **Python 3.9+**
- **Git** for version control
- **Android Studio** (for Android development)
- **Xcode** (for iOS development on macOS)

### Installation Commands

#### Windows

```bash
# Install Node.js (download from https://nodejs.org/)
# Install Python (download from https://www.python.org/)

# Verify installations
node --version
npm --version
python --version
```

#### macOS

```bash
# Using Homebrew
brew install node
brew install python

# Verify
node --version
npm --version
python3 --version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y nodejs npm python3 python3-venv python3-pip

# Verify
node --version
npm --version
python3 --version
```

---

## Frontend Setup

### Step 1: Install Dependencies

```bash
# Navigate to project root
cd pothole-detector

# Install Node packages
npm install
```

### Step 2: Install Expo CLI Globally

```bash
# Install Expo CLI
npm install -g expo-cli

# Verify installation
expo --version
```

### Step 3: Configure Environment Variables

Create `.env` file in the project root:

```env
# Backend API Configuration
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_API_TIMEOUT=30000

# Map Configuration
EXPO_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

### Step 4: Start Development Server

```bash
# Start Expo development server
npx expo start
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Backend Environment

Create `.env` file in `backend/` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Model Configuration
MODEL_PATH=./yolov8n.pt
CONFIDENCE_THRESHOLD=0.5

# CORS
CORS_ORIGINS=["http://localhost:19000"]
```

### Step 5: Verify Backend Installation

```bash
# Test FastAPI
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

# Test YOLOv8
python -c "from ultralytics import YOLO; print('YOLOv8 ready')"
```

---

## Running the Application

### Terminal 1 - Frontend

```bash
cd pothole-detector
npx expo start
```

### Terminal 2 - Backend

```bash
cd pothole-detector/backend
.venv\Scripts\Activate.ps1  # Windows
# OR
source .venv/bin/activate    # macOS/Linux

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Testing

### Backend API Testing

```bash
# Health check
curl http://localhost:8000/health

# API docs
# Visit: http://localhost:8000/docs
```

---

## Troubleshooting

### Backend Issues

#### Problem: Model not loading

```bash
# Download model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### Problem: Port 8000 already in use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

#### Problem: CORS error

```bash
# Update .env
CORS_ORIGINS=["http://localhost:19000","*"]
```

---

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment options.

---

**Happy detecting!**
