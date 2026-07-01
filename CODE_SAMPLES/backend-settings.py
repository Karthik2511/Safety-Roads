"""
Configuration Management - Python
Demonstrates: Environment variable handling, settings dataclass, path resolution
 
Key patterns:
- Dataclass for clean configuration structure
- Environment variable loading with .env file
- Configurable thresholds for ML model inference
- Path resolution for model loading
- Type safety with Python 3.10+ features
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

BACKEND_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    """Configuration settings from environment variables"""
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Model configuration
    model_path: str = os.getenv(
        "MODEL_PATH", "./runs/detect/pothole_yolov83/weights/best.pt"
    )
    model_url: str | None = os.getenv("MODEL_URL")
    
    # Detection thresholds
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.4"))
    min_box_area_ratio: float = float(os.getenv("MIN_BOX_AREA_RATIO", "0.01"))
    max_box_area_ratio: float = float(os.getenv("MAX_BOX_AREA_RATIO", "0.35"))
    max_box_aspect_ratio: float = float(os.getenv("MAX_BOX_ASPECT_RATIO", "3.0"))
    
    # Class names configuration
    pothole_class_names: tuple[str, ...] = tuple(
        x.strip().lower()
        for x in os.getenv("POTHOLE_CLASS_NAMES", "pothole,potholes").split(",")
        if x.strip()
    )
    
    # Debug flags
    debug_raw_boxes: bool = os.getenv("DEBUG_RAW_BOXES", "false").strip().lower() in (
        "1", "true", "yes", "on"
    )
    debug_top_k: int = int(os.getenv("DEBUG_TOP_K", "5"))

    def resolve_model_path(self) -> Path:
        """Resolve the model path from configuration"""
        configured_path = Path(self.model_path)
        candidates: list[Path] = []

        if configured_path.is_absolute():
            candidates.append(configured_path)
        else:
            candidates.extend([
                BACKEND_DIR / configured_path, 
                Path.cwd() / configured_path
            ])

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()
        
        raise FileNotFoundError(f"Model not found in any candidate path: {candidates}")


# Global settings instance
settings = Settings()
