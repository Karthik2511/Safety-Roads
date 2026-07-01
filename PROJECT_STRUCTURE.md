# 📁 Project Structure Guide

Complete overview of the codebase organization.

## Directory Structure

```
pothole-detector/
│
├── 📱 FRONTEND (React Native/Expo)
│   ├── app/
│   │   ├── (tabs)/
│   │   │   ├── index.tsx          # Home screen
│   │   │   ├── explore.tsx        # Map screen
│   │   │   └── report.tsx         # Report screen
│   │   ├── _layout.tsx            # Navigation
│   │   └── modal.tsx              # Modal components
│   │
│   ├── components/                # Reusable components
│   │   ├── external-link.tsx
│   │   ├── parallax-scroll-view.tsx
│   │   ├── themed-text.tsx
│   │   └── ui/
│   │
│   ├── services/                  # Business logic
│   │   ├── api.ts                 # HTTP client
│   │   ├── potholeDetection.ts    # Detection logic
│   │   └── storage.ts             # Local storage
│   │
│   ├── hooks/                     # Custom React hooks
│   ├── constants/                 # App constants
│   ├── assets/                    # Static assets
│   │
│   ├── app.json                   # Expo configuration
│   ├── package.json               # Dependencies
│   ├── tsconfig.json              # TypeScript config
│   ├── babel.config.js            # Babel config
│   └── eslint.config.js           # ESLint config
│
├── 🐍 BACKEND (Python/FastAPI)
│   ├── main.py                    # FastAPI application
│   ├── app/
│   │   ├── model.py               # YOLOv8 model
│   │   ├── schemas.py             # Pydantic schemas
│   │   └── settings.py            # Configuration
│   │
│   ├── data/                      # Dataset config
│   ├── datasets/                  # Training data
│   ├── runs/                      # Training results
│   ├── requirements.txt           # Python dependencies
│   └── yolov8n.pt                 # Model weights
│
├── 📸 SHOWCASE
│   ├── Imgs/                      # Screenshots
│   └── GITHUB_PORTFOLIO/          # Portfolio docs
│
├── 🔧 CONFIGURATION
│   ├── app.json                   # Expo config
│   ├── package.json               # Frontend deps
│   ├── tsconfig.json              # TS config
│   ├── .gitignore                 # Git ignore
│   └── babel.config.js            # Babel config
│
├── android/                       # Android native
│   ├── app/
│   │   ├── src/
│   │   └── build.gradle
│   └── settings.gradle
│
└── 📚 DOCUMENTATION
    ├── README.md
    ├── ARCHITECTURE.md
    ├── SETUP_GUIDE.md
    ├── API_DOCUMENTATION.md
    ├── DEPLOYMENT.md
    └── LICENSE
```

---

## Key Files Explained

### Frontend

**app/(tabs)/index.tsx**

- Main detection screen
- Camera integration
- Real-time detection display

**services/api.ts**

- HTTP client for backend
- Handles detection requests

**services/potholeDetection.ts**

- Detection business logic
- Result processing

### Backend

**main.py**

- FastAPI application
- Route definitions
- Server startup

**app/model.py**

- YOLOv8 model wrapper
- Inference logic
- Severity classification

**app/schemas.py**

- Pydantic request/response models
- Input validation

### Configuration

**app.json**

- Expo project configuration
- Permissions, plugins
- Build settings

**package.json**

- Frontend dependencies
- npm scripts
- Version info

---

## File Sizes

- Frontend code: ~2MB
- Backend code: ~1MB
- YOLOv8 model: 6.3MB
- Total codebase: ~9MB (excluding node_modules)

---

## Navigation Guide

### For Frontend Development

Start with: `app/(tabs)/index.tsx`

### For Backend Development

Start with: `backend/main.py`

### For API Integration

See: `services/api.ts`

### For Model Details

See: `backend/app/model.py`

---

**Complete and well-organized!**
