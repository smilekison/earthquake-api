import unittest
from app.redis_client import get_redis_client
from app.config import REDIS_HOST, REDIS_PORT

class TestRedisClient(unittest.TestCase):
    def test_redis_connection(self):
        # Test that the Redis connection is successfully established
        redis_client = get_redis_client()

        # Check if the Redis client is not None
        self.assertIsNotNone(redis_client, "Redis client should not be None")

        # Check if the Redis client can ping the server
        self.assertTrue(redis_client.ping(), "Redis server should respond to ping")

        # Optionally, you can print the Redis connection details for debugging
        print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")

    def test_redis_set_get(self):
        # Test basic Redis SET and GET operations
        redis_client = get_redis_client()

        # Define a test key and value
        test_key = "test_key"
        test_value = "test_value"

        # Set a value in Redis
        redis_client.set(test_key, test_value)

        # Get the value from Redis
        retrieved_value = redis_client.get(test_key)

        # Check if the retrieved value matches the original value
        self.assertEqual(retrieved_value, test_value, f"Expected value '{test_value}' for key '{test_key}'")

        # Clean up: Delete the test key from Redis
        redis_client.delete(test_key)

if __name__ == "__main__":
    unittest.main()