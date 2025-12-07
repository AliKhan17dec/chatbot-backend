"""
FastAPI application for Humanoid Robotics Book RAG Chatbot.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from config import settings
from routers import chat
from models.schemas import HealthResponse
from services.qdrant_service import qdrant_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Humanoid Robotics Book Chatbot API...")
    logger.info(f"Environment: {settings.app_env}")
    
    # Initialize services
    try:
        # Check Qdrant connection
        qdrant_connected = qdrant_service.check_connection()
        if qdrant_connected:
            logger.info("✓ Qdrant connection successful")
        else:
            logger.warning("✗ Qdrant connection failed")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Humanoid Robotics Book Chatbot API...")


# Create FastAPI app
app = FastAPI(
    title="Humanoid Robotics Book Chatbot API",
    description="RAG-based chatbot API for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Humanoid Robotics Book Chatbot API",
        "version": "1.0.0",
        "description": "RAG-based chatbot for Physical AI & Humanoid Robotics textbook",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check Qdrant connection
        qdrant_connected = qdrant_service.check_connection()
        
        # For now, we'll skip database check since it's optional
        # You can add Neon Postgres check here if needed
        database_connected = True
        
        status = "healthy" if (qdrant_connected and database_connected) else "degraded"
        
        return HealthResponse(
            status=status,
            qdrant_connected=qdrant_connected,
            database_connected=database_connected,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            qdrant_connected=False,
            database_connected=False,
            timestamp=datetime.utcnow()
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc) if settings.app_env == "development" else "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.app_env == "development" else False
    )
