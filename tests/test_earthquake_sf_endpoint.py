import pytest
import requests
from datetime import datetime, timedelta, timezone

# Base URL of the API
BASE_URL = "http://localhost:8000"

def test_successful_response():
    """
    Test that the endpoint returns a successful response with valid input parameters.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 2.0,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "type" in data, "Response should contain 'type'"
    assert "features" in data, "Response should contain 'features'"
    assert data["type"] == "FeatureCollection", "Expected type to be 'FeatureCollection'"

def test_min_magnitude_filter():
    """
    Test that the endpoint filters earthquakes based on the min_magnitude parameter.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 5.0,  # Only earthquakes with magnitude >= 5.0
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"].get("mag", 0) >= 5.0, "All earthquakes should have magnitude >= 5.0"

def test_invalid_date_format():
    """
    Test that the endpoint returns a 400 error for invalid date formats.
    """
    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": "invalid-date",
            "end_time": "2024-01-01T00:00:00",
            "min_magnitude": 2.0,
        },
    )

    assert response.status_code == 400, "Expected status code 400 for invalid date format"

def test_no_earthquakes_found():
    """
    Test that the endpoint returns an empty features list when no earthquakes match the criteria.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 10.0,  # Unrealistically high magnitude
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert len(data["features"]) == 0, "Expected no earthquakes to match the criteria"

def test_response_format_json():
    """
    Test that the endpoint returns data in JSON format when requested.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 2.0,
            "format": "json",
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    assert response.headers["Content-Type"] == "application/json", "Expected JSON response"

def test_response_format_xml():
    """
    Test that the endpoint returns data in XML format when requested.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 2.0,
            "format": "xml",
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    assert response.headers["Content-Type"] == "application/xml", "Expected XML response"

def test_large_time_range():
    """
    Test that the endpoint handles large time ranges without errors.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=365)  # 1 year
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 2.0,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "features" in data, "Response should contain 'features'"

def test_edge_case_min_magnitude_zero():
    """
    Test that the endpoint returns all earthquakes when min_magnitude is 0.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake/sf",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_magnitude": 0,  # Return all earthquakes
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"].get("mag", 0) >= 0, "All earthquakes should have magnitude >= 0"