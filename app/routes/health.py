from fastapi import APIRouter
from datetime import datetime
from app.redis_client import redis_client

router = APIRouter()

@router.get("/")
def health_check():
    """
    Health check endpoint to verify the service status and Redis connection.
    """
    cache_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "cache_status": cache_status
    }
