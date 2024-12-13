from fastapi import APIRouter
from datetime import datetime
from app.redis_client import redis_client

router = APIRouter()

"""
    Purpose: Monitors the health status of the API service and its dependencies
    
    What it does:
    - Checks if Redis cache is connected and responding
    - Gets current UTC timestamp
    - Returns service health status information
    
    Parameters: None
    
    Returns: Dictionary containing:
    - status: Service health status
    - timestamp: Current UTC time
    - cache_status: Redis connection status ('connected' or 'disconnected')
    
    Used for: Monitoring system health and detecting service issues
"""
@router.get("/")
def health_check():
    # Check if Redis is connected and responding to ping
    # Returns 'connected' if Redis client exists and responds to ping
    # Returns 'disconnected' if Redis is not available or not responding
    cache_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    
    # Return health status object with:
        # - Current service status
        # - UTC timestamp for when check was performed
        # - Current Redis connection status
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "cache_status": cache_status
    }
