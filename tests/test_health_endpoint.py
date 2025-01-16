import pytest
import requests
from datetime import datetime, timezone

# Base URL of the API
BASE_URL = "http://localhost:8000"

def test_successful_response():
    """
    Test that the endpoint returns a successful response.
    """
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "status" in data, "Response should contain 'status'"
    assert "timestamp" in data, "Response should contain 'timestamp'"
    assert "cache_status" in data, "Response should contain 'cache_status'"
    assert data["status"] == "healthy", "Expected status to be 'healthy'"

def test_cache_status():
    """
    Test that the cache_status is either 'connected' or 'disconnected'.
    """
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert data["cache_status"] in ["connected", "disconnected"], "cache_status should be 'connected' or 'disconnected'"
