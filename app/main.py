"""
Main application module for the Earthquake API Service
Initializes FastAPI application, sets up routes, and configures Redis connection
Acts as the entry point for the web service
"""

# This is the main control center of our earthquake information service

from fastapi import FastAPI
from app.routes import earthquakes, tsunami, health, earthquake_felt
from app.logger import setup_logging
from app.redis_client import get_redis_client  # Import the Redis client initialization
import uvicorn


# Set up logging for the application
logger = setup_logging()

# Create our web application using FastAPI
app = FastAPI(title="Earthquake API Service")

# Connect to our memory helper (Redis)
redis_client = get_redis_client()

# Include routers
# Tell our app about all the different services we offer
app.include_router(earthquakes.router, tags=["Earthquakes"])
app.include_router(earthquake_felt.router, tags=["Earthquakes-felt"])
app.include_router(tsunami.router,tags=["Tsunami Alerts"])
app.include_router(health.router, tags=["Health"])


# This code runs when we start the program directly
if __name__ == "__main__":
    # Check if Redis connection was successful
    if redis_client:
        # Check Connection with the Redis-Server
        logger.info("Redis connection is successful.")
    else:
        logger.warning("Redis connection failed.")

    # Start our web service
    # Tell it to listen for requests from anywhere (0.0.0.0) on port number 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
