import unittest
import requests

class TestHealthEndpoint(unittest.TestCase):
    BASE_URL = "http://localhost:8000"  # Base URL of your API

    def test_health_endpoint(self):
        # Make a GET request to the /health endpoint
        response = requests.get(f"{self.BASE_URL}/")
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, "Expected status code 200")

        # Parse the JSON response
        data = response.json()

        # Check if the response contains the expected keys
        self.assertIn("status", data, "Response should contain 'status'")
        self.assertIn("timestamp", data, "Response should contain 'timestamp'")
        self.assertIn("cache_status", data, "Response should contain 'cache_status'")

        # Check if the status is "healthy"
        self.assertEqual(data["status"], "healthy", "Expected status to be 'healthy'")

        # Check if cache_status is either "connected" or "disconnected"
        self.assertIn(data["cache_status"], ["connected", "disconnected"], "cache_status should be 'connected' or 'disconnected'")

        # Optionally, you can print the response for debugging
        print("Health Check Response:", data)

if __name__ == "__main__":
    unittest.main()