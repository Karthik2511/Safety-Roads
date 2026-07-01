"""
API Request/Response Data Models - Pydantic
Demonstrates: Type-safe data validation, API contract definition
 
Key patterns:
- Pydantic BaseModel for automatic validation
- Field descriptions for API documentation
- Union types for flexible responses
- Type hints for clarity
"""

from pydantic import BaseModel, Field


class DetectPayload(BaseModel):
    """Request payload for pothole detection endpoint"""
    image: str = Field(..., description="Base64 encoded image")
    lat: float = Field(..., description="GPS latitude coordinate")
    lon: float = Field(..., description="GPS longitude coordinate")


class BoundingBox(BaseModel):
    """Bounding box coordinates for detected object"""
    x: float = Field(..., description="X coordinate (pixels)")
    y: float = Field(..., description="Y coordinate (pixels)")
    width: float = Field(..., description="Box width (pixels)")
    height: float = Field(..., description="Box height (pixels)")


class PotholeDetection(BaseModel):
    """Single pothole detection result"""
    confidence: float = Field(..., description="Confidence score 0.0-1.0")
    bbox: BoundingBox = Field(..., description="Bounding box location")
    class_name: str = Field(..., description="Object class (e.g., 'pothole')")
    pothole_type: str = Field(..., description="Type classification")
    severity: str = Field(..., description="Severity level: High/Medium/Low")


class DetectResponse(BaseModel):
    """Response from pothole detection endpoint"""
    pothole: bool = Field(..., description="Whether pothole detected")
    detected: bool = Field(..., description="Detection flag")
    pothole_count: int = Field(default=0, description="Number of potholes found")
    detections: list[PotholeDetection] = Field(
        default_factory=list, 
        description="List of detected potholes"
    )
    confidence: float = Field(..., description="Highest confidence score")
    bbox: BoundingBox | None = Field(
        default=None, 
        description="Highest confidence bounding box"
    )
    class_name: str | None = None
    pothole_type: str | None = None
    severity: str | None = None
    lat: float = Field(..., description="GPS latitude from request")
    lon: float = Field(..., description="GPS longitude from request")
