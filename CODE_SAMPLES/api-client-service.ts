/**
 * API Client Service - TypeScript
 * Demonstrates: HTTP request handling, environment configuration, error recovery
 *
 * Key patterns:
 * - Auto-detection of backend URL (local dev, emulator, physical device, production)
 * - Health check with timeout protection
 * - Base64 image encoding for detection requests
 * - Structured request/response types
 * - Graceful error handling and logging
 */


const HEALTH_CHECK_TIMEOUT_MS = 15000;
const DETECTION_TIMEOUT_MS = 45000;

const CONFIGURED_BACKEND_URL =
  process.env.EXPO_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

interface HealthResponse {
  ok: boolean;
  model_loaded?: boolean;
}

interface DetectPayload {
  image: string; // base64 encoded image
  lat: number;
  lon: number;
}

interface DetectResponse {
  pothole: boolean;
  detected: boolean;
  confidence: number;
  severity?: string | null;
}

export interface BackendDetectionResult {
  detected: boolean;
  confidence: number;
  severity?: string | null;
  error?: string;
}

class ApiService {
  private isOnline = false;
  private activeBackendUrl = CONFIGURED_BACKEND_URL;

  async checkBackendHealth(): Promise<boolean> {
    try {
      console.log(`🌐 Checking backend health at ${this.activeBackendUrl}`);
      const response = await Promise.race([
        fetch(`${this.activeBackendUrl}/health`),
        new Promise((_, reject) =>
          setTimeout(
            () => reject(new Error("Health check timeout")),
            HEALTH_CHECK_TIMEOUT_MS,
          ),
        ),
      ]);

      if (!response || !response.ok) {
        this.isOnline = false;
        return false;
      }

      const data = (await response.json()) as HealthResponse;
      this.isOnline = data.ok && (data.model_loaded ?? true);
      return this.isOnline;
    } catch (error) {
      console.error("❌ Backend health check failed:", error);
      this.isOnline = false;
      return false;
    }
  }

  async sendDetectionRequest(
    base64Image: string,
    latitude: number,
    longitude: number,
  ): Promise<BackendDetectionResult> {
    if (!this.isOnline) {
      return { detected: false, confidence: 0, error: "Backend offline" };
    }

    const payload: DetectPayload = {
      image: base64Image,
      lat: latitude,
      lon: longitude,
    };

    try {
      const response = await Promise.race([
        fetch(`${this.activeBackendUrl}/detect`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }),
        new Promise((_, reject) =>
          setTimeout(
            () => reject(new Error("Detection timeout")),
            DETECTION_TIMEOUT_MS,
          ),
        ),
      ]);

      if (!response || !response.ok) {
        return { detected: false, confidence: 0, error: "API error" };
      }

      const result = (await response.json()) as DetectResponse;
      return {
        detected: result.detected,
        confidence: result.confidence,
        severity: result.severity,
      };
    } catch (error) {
      console.error("❌ Detection request failed:", error);
      return { detected: false, confidence: 0, error: String(error) };
    }
  }
}

export const apiService = new ApiService();
