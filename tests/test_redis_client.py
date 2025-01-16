import pytest
from app.redis_client import get_redis_client
from app.config import REDIS_HOST, REDIS_PORT

def test_redis_connection():
    """
    Test that the Redis client can connect to the Redis server.
    """
    redis_client = get_redis_client()
    assert redis_client is not None, "Redis client should not be None"
    assert redis_client.ping(), "Redis server should respond to ping"

def test_redis_set_get():
    """
    Test that the Redis client can set and retrieve a key-value pair.
    """
    redis_client = get_redis_client()
    test_key = "test_key"
    test_value = "test_value"

    # Set a value in Redis
    redis_client.set(test_key, test_value)

    # Get the value from Redis
    retrieved_value = redis_client.get(test_key)
    assert retrieved_value == test_value, f"Expected value '{test_value}' for key '{test_key}'"

    # Clean up: Delete the test key from Redis
    redis_client.delete(test_key)

def test_redis_connection_failure():
    """
    Test that the Redis client handles connection failures gracefully.
    """
    # Temporarily change the Redis host to an invalid one
    original_host = REDIS_HOST
    try:
        # Simulate a connection failure by using an invalid host
        import os
        os.environ["REDIS_HOST"] = "invalid_host"
        from app.redis_client import get_redis_client

        redis_client = get_redis_client()
        assert redis_client is None, "Expected Redis client to be None due to connection failure"
    finally:
        # Restore the original Redis host
        os.environ["REDIS_HOST"] = original_host