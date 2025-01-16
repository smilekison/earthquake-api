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
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 10,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "type" in data, "Response should contain 'type'"
    assert "features" in data, "Response should contain 'features'"
    assert data["type"] == "FeatureCollection", "Expected type to be 'FeatureCollection'"

def test_min_felt_reports_filter():
    """
    Test that the endpoint filters earthquakes based on the min_felt_reports parameter.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 50,  # Only earthquakes with >= 50 felt reports
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"].get("felt", 0) >= 50, "All earthquakes should have >= 50 felt reports"

def test_invalid_date_format():
    """
    Test that the endpoint returns a 400 error for invalid date formats.
    """
    response = requests.get(
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": "invalid-date",
            "end_time": "2024-01-01T00:00:00",
            "min_felt_reports": 10,
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
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 1000,  # Unrealistically high number
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
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 10,
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
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 10,
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
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 10,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "features" in data, "Response should contain 'features'"

def test_edge_case_min_felt_reports_zero():
    """
    Test that the endpoint returns all earthquakes with any felt reports when min_felt_reports is 0.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time_str,
            "end_time": end_time_str,
            "min_felt_reports": 0,  # Return all earthquakes with any felt reports
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"].get("felt", 0) >= 0, "All earthquakes should have >= 0 felt reports"

def test_large_dataset_performance():
    """
    Test the performance of the API when requesting a large dataset (e.g., 2014 to 2024).
    """
    start_time = "2004-01-01T00:00:00"
    end_time = "2024-01-01T00:00:00"
    min_felt_reports = 2  # Adjust as needed

    # Measure the time taken to process the request
    import time
    start = time.time()

    response = requests.get(
        f"{BASE_URL}/earthquake-felt",
        params={
            "start_time": start_time,
            "end_time": end_time,
            "min_felt_reports": min_felt_reports,
        },
    )

    end = time.time()
    elapsed_time = end - start

    # Check if the response is successful
    assert response.status_code == 200, "Expected status code 200"

    # Check the size of the response
    response_size = len(response.content)  # Size in bytes
    print(f"Response size: {response_size} bytes")
    print(f"Time taken: {elapsed_time} seconds")

    # Optionally, set a limit for response size and time
    MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_RESPONSE_TIME = 30  # 30 seconds

    assert response_size <= MAX_RESPONSE_SIZE, f"Response size exceeds {MAX_RESPONSE_SIZE} bytes"
    assert elapsed_time <= MAX_RESPONSE_TIME, f"Response time exceeds {MAX_RESPONSE_TIME} seconds"