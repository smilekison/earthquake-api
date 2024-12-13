import redis
from app.logger import setup_logging
from app.config import REDIS_HOST, REDIS_PORT

logger = setup_logging()


def get_redis_client():
    """Create and return a Redis client."""
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0,
            decode_responses=True,
            socket_connect_timeout=5
        )
        if client.ping():
            logger.info(f"✅ Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        else:
            logger.warning("⚠️ Redis ping failed")
            return None
    except redis.ConnectionError as e:
        logger.warning(f"⚠️ Failed to connect to Redis: {str(e)}")
        return None
    except Exception as e:
        logger.warning(f"⚠️ Unexpected error connecting to Redis: {str(e)}")
        return None
    return client
redis_client = get_redis_client()