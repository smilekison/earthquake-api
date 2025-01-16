import unittest
import requests
from datetime import datetime, timedelta, timezone

class TestTsunamiEndpoint(unittest.TestCase):
    BASE_URL = "http://localhost:8000"  # Base URL of your API

    def test_tsunami_endpoint(self):
        # Define test parameters using timezone-aware datetime objects
        state = "SF"  # Test for California
        start_time = datetime.now(timezone.utc)  # Current time in UTC
        time_range = 24  # Look back 24 hours
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Make a GET request to the /{state} tsunami endpoint
        response = requests.get(
            f"{self.BASE_URL}/{state}",
            params={
                "start_time": start_time_str,
                "time_range": time_range,
            },
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, "Expected status code 200")

        # Parse the JSON response
        data = response.json()

        # Check if the response contains the expected structure
        self.assertIn("type", data, "Response should contain 'type'")
        self.assertIn("metadata", data, "Response should contain 'metadata'")
        self.assertIn("features", data, "Response should contain 'features'")

        # Check if the type is "FeatureCollection"
        self.assertEqual(data["type"], "FeatureCollection", "Expected type to be 'FeatureCollection'")

        # Check if metadata contains the state and time range
        self.assertIn("state", data["metadata"], "Metadata should contain 'state'")
        self.assertEqual(data["metadata"]["state"], state, f"Expected state to be {state}")

        # Check if features is a list
        self.assertIsInstance(data["features"], list, "Expected 'features' to be a list")

        # Optionally, you can print the response for debugging
        print("Tsunami Response:", data)

if __name__ == "__main__":
    unittest.main()