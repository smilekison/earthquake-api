
# Importing the library and other files from package
import redis
from app.logger import setup_logging
from app.config import REDIS_HOST, REDIS_PORT

# Start our program's diary
logger = setup_logging()


"""
    Purpose: Establishes connection with Redis database
    What it does:
    - Attempts to create a connection to Redis using configured host and port
    - Verifies connection with a ping test
    - Handles connection failures with logs
    - Logs connection status (success/failure)
    Returns: 
    - Redis client object if connection successful
    - None if connection fails
    Used for: Caching earthquake data to improve performance
"""

def get_redis_client():
    """Create and return a Redis client - Making a new connection to our server."""
    try:
        client = redis.Redis(
            host=REDIS_HOST,          # Where to find Redis
            port=REDIS_PORT,          # Which port to use
            db=0,                     # Which datbase to use (0 is the first one)
            decode_responses=True,     # Tell Redis to give us readable text back
            socket_connect_timeout=5   # Give up waiting after 5 seconds
        )
        # Check if Redis is responding by sending it a "ping"
        if client.ping():
            logger.info(f"✅ Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return client
        else:
            logger.warning("⚠️ Redis ping failed")
            return None
    except redis.ConnectionError as e:
        # If something goes wrong while connecting, write a log
        logger.warning(f"⚠️ Failed to connect to Redis: {str(e)}")
        return None
    
# Try to connect to Redis right away when this file is loaded
redis_client = get_redis_client()