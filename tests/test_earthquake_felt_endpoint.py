import unittest
import requests
from datetime import datetime, timedelta, timezone

class TestEarthquakeFeltEndpoint(unittest.TestCase):
    BASE_URL = "http://localhost:8000"  # Base URL of your API

    def test_earthquake_felt_endpoint(self):
        # Define test parameters using timezone-aware datetime objects
        end_time = datetime.now(timezone.utc)  # Current time in UTC
        start_time = end_time - timedelta(days=1)  # Look back 1 day
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        min_felt_reports = 10  # Minimum number of felt reports

        # Make a GET request to the /earthquake-felt endpoint
        response = requests.get(
            f"{self.BASE_URL}/earthquake-felt",
            params={
                "start_time": start_time_str,
                "end_time": end_time_str,
                "min_felt_reports": min_felt_reports,
            },
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, "Expected status code 200")

        # Parse the JSON response
        data = response.json()

        # Check if the response contains the expected structure
        self.assertIn("type", data, "Response should contain 'type'")
        self.assertIn("features", data, "Response should contain 'features'")

        # Check if the type is "FeatureCollection"
        self.assertEqual(data["type"], "FeatureCollection", "Expected type to be 'FeatureCollection'")

        # Check if features is a list
        self.assertIsInstance(data["features"], list, "Expected 'features' to be a list")

        # Optionally, you can print the response for debugging
        print("Earthquake Felt Response:", data)

if __name__ == "__main__":
    unittest.main()