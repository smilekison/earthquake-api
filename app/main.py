# app/main.py
from fastapi import FastAPI
from app.routes import earthquakes, tsunami, health, earthquake_felt
from app.logger import setup_logging
from app.redis_client import get_redis_client  # Import the Redis client initialization

# Set up logging
setup_logging()

# Create FastAPI app
app = FastAPI(title="Earthquake API Service")


# Initialize Redis client
redis_client = get_redis_client()

# Include routers
app.include_router(earthquakes.router, tags=["Earthquakes"])
app.include_router(earthquake_felt.router, tags=["Earthquakes-felt"])
app.include_router(tsunami.router,tags=["Tsunami Alerts"])
app.include_router(health.router, tags=["Health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
