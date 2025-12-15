"""
ShowUp - Appointment No-Show Predictor
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers (we'll create these later)
# from app.api import appointments, predictions, analytics

# Create FastAPI app
app = FastAPI(
    title="ShowUp API",
    description="AI-powered appointment no-show prediction and reminder system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "message": "ShowUp API is running",
        "version": "1.0.0"
    }

# Root API info
@app.get("/api")
async def api_info():
    """
    API information and available endpoints.
    """
    return {
        "name": "ShowUp API",
        "version": "1.0.0",
        "description": "AI-powered appointment no-show prediction and reminder system",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "appointments": "/api/appointments (coming soon)",
            "predictions": "/api/predictions (coming soon)",
            "analytics": "/api/analytics (coming soon)"
        }
    }

# Include routers (uncomment as we build them)
from app.api import appointments
app.include_router(appointments.router, prefix="/api/appointments", tags=["appointments"])
# app.include_router(appointments.router, prefix="/api/appointments", tags=["appointments"])
# app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
# app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the application starts.
    """
    print("🚀 ShowUp API starting up...")
    print("📊 Environment:", os.getenv("ENVIRONMENT", "development"))
    print("✅ API running at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform when the application shuts down.
    """
    print("👋 ShowUp API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (development only)
    )
