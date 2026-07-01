"""
FastAPI Application Entry Point - Python
Demonstrates: RESTful API structure, endpoint design, error handling
 
Key patterns:
- FastAPI with Pydantic validation
- Application lifecycle management (startup event)
- Health check endpoint for monitoring
- Detection endpoint with error handling
- Graceful degradation when model unavailable

NOTE: Model inference logic (app.model.create_detector) is proprietary
and not included in this sample. This shows the API architecture.
"""

try:
    # Supports running as package: uvicorn backend.main:app
    from .app.model import create_detector
    from .app.schemas import DetectPayload, DetectResponse
    from .app.settings import settings
except ImportError:
    # Supports running from backend dir: uvicorn main:app
    from app.model import create_detector
    from app.schemas import DetectPayload, DetectResponse
    from app.settings import settings

from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI(title="Pothole YOLOv8 API", version="1.0.0")


@app.on_event("startup")
def load_model() -> None:
    """Load ML model on server startup"""
    try:
        app.state.detector = create_detector()
        print(f"✅ Loaded model from {settings.model_path}")
    except FileNotFoundError as exc:
        app.state.detector = None
        print(f"⚠️  Warning: {exc}")


@app.get("/health")
def health() -> dict:
    """Health check endpoint for monitoring"""
    detector = getattr(app.state, "detector", None)
    return {
        "ok": True,
        "model_loaded": detector is not None,
        "model_path": settings.model_path,
        "confidence_threshold": settings.confidence_threshold,
    }


@app.post("/detect", response_model=DetectResponse)
def detect(payload: DetectPayload) -> DetectResponse:
    """
    Main pothole detection endpoint
    
    Request: Base64 encoded image + GPS coordinates
    Response: Detection results with bounding boxes and severity
    """
    detector = getattr(app.state, "detector", None)
    
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Check MODEL_PATH and restart server.",
        )

    try:
        # Decode image from base64
        image_array = detector.decode_image(payload.image)
        
        # Run inference
        result = detector.infer(image_array)
        
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc

    # Format detections for response
    pothole_detections = []
    if result.get("detections"):
        for det in result["detections"]:
            pothole_detections.append({
                "confidence": det["confidence"],
                "bbox": det["bbox"],
                "class_name": det["class_name"],
                "pothole_type": det["pothole_type"],
                "severity": det["severity"],
            })

    return DetectResponse(
        pothole=result["detected"],
        detected=result["detected"],
        pothole_count=len(pothole_detections),
        detections=pothole_detections,
        confidence=result["confidence"],
        bbox=result["bbox"],
        class_name=result["class_name"],
        pothole_type=result.get("pothole_type"),
        severity=result.get("severity"),
        lat=payload.lat,
        lon=payload.lon,
    )
