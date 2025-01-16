import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import REDIS_HOST, REDIS_PORT, CACHE_DURATION, USGS_API_URL

class TestConfig(unittest.TestCase):
    def test_redis_host(self):
        # Test that REDIS_HOST is correctly set (default or from environment)
        expected_host = os.getenv("REDIS_HOST", "localhost")
        self.assertEqual(REDIS_HOST, expected_host, f"Expected REDIS_HOST to be {expected_host}")

    def test_redis_port(self):
        # Test that REDIS_PORT is correctly set (default or from environment)
        expected_port = int(os.getenv("REDIS_PORT", 6379))
        self.assertEqual(REDIS_PORT, expected_port, f"Expected REDIS_PORT to be {expected_port}")

    def test_cache_duration(self):
        # Test that CACHE_DURATION is correctly set
        self.assertEqual(CACHE_DURATION, 30, "Expected CACHE_DURATION to be 30 seconds")

    def test_usgs_api_url(self):
        # Test that USGS_API_URL is correctly set
        expected_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.assertEqual(USGS_API_URL, expected_url, f"Expected USGS_API_URL to be {expected_url}")

if __name__ == "__main__":
    unittest.main()