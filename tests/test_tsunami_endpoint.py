import pytest
import requests
from datetime import datetime, timedelta, timezone

# Base URL of the API
BASE_URL = "http://localhost:8000"

def test_successful_response():
    """
    Test that the endpoint returns a successful response with valid input parameters.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 24  # Look back 24 hours
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "type" in data, "Response should contain 'type'"
    assert "metadata" in data, "Response should contain 'metadata'"
    assert "features" in data, "Response should contain 'features'"
    assert data["type"] == "FeatureCollection", "Expected type to be 'FeatureCollection'"

def test_tsunami_filter():
    """
    Test that the endpoint filters earthquakes based on the tsunami property.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 24  # Look back 24 hours
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"].get("tsunami", 0) > 0, "All earthquakes should have tsunami > 0"

def test_invalid_date_format():
    """
    Test that the endpoint returns a 400 error for invalid date formats.
    """
    state = "CA"  # Test for California
    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": "invalid-date",
            "time_range": 24,
        },
    )

    assert response.status_code == 400, "Expected status code 400 for invalid date format"

# def test_invalid_time_range():
#     """
#     Test that the endpoint returns a 400 error for invalid time ranges.
#     """
#     state = "sf"  # Test for sanfrancisco
#     start_time = datetime.now(timezone.utc)
#     start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

#     # Test with a negative time range
#     response = requests.get(
#         f"{BASE_URL}/{state}",
#         params={
#             "start_time": start_time_str,
#             "time_range": -1,
#         },
#     )

#     assert response.status_code == 400, "Expected status code 400 for invalid time range"

#     # Test with a time range greater than 168 hours
#     response = requests.get(
#         f"{BASE_URL}/{state}",
#         params={
#             "start_time": start_time_str,
#             "time_range": 169,
#         },
#     )

#     assert response.status_code == 422, "Expected status code 422 for invalid time range"

def test_no_tsunami_alerts_found():
    """
    Test that the endpoint returns an empty features list when no tsunami alerts match the criteria.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 24  # Look back 24 hours
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert len(data["features"]) == 0, "Expected no tsunami alerts to match the criteria"

def test_response_format_json():
    """
    Test that the endpoint returns data in JSON format when requested.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 24  # Look back 24 hours
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
            "format": "json",
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    assert response.headers["Content-Type"] == "application/json", "Expected JSON response"

def test_response_format_xml():
    """
    Test that the endpoint returns data in XML format when requested.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 24  # Look back 24 hours
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
            "format": "xml",
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    assert response.headers["Content-Type"] == "application/xml", "Expected XML response"

def test_large_time_range():
    """
    Test that the endpoint handles large time ranges without errors.
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 168  # Maximum valid time range (168 hours)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "features" in data, "Response should contain 'features'"

def test_edge_case_time_range_min():
    """
    Test that the endpoint handles the minimum valid time range (1 hour).
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 1  # Minimum valid time range (1 hour)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "features" in data, "Response should contain 'features'"

def test_edge_case_time_range_max():
    """
    Test that the endpoint handles the maximum valid time range (168 hours).
    """
    state = "CA"  # Test for California
    start_time = datetime.now(timezone.utc)
    time_range = 168  # Maximum valid time range (168 hours)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    response = requests.get(
        f"{BASE_URL}/{state}",
        params={
            "start_time": start_time_str,
            "time_range": time_range,
        },
    )

    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert "features" in data, "Response should contain 'features'"