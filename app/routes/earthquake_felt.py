from fastapi import APIRouter, Query
from app.utils import fetch_usgs_data, format_response, validate_date
from app.redis_client import get_redis_client

# Create a router instance to manage our earthquake-felt endpoints
router = APIRouter()

"""
    Purpose: Retrieves earthquakes in SF Bay Area that have been reported as felt by people
    
    What it does:
    - Validates input date parameters
    - Fetches earthquake data within 100km radius of San Francisco
    - Filters earthquakes based on minimum number of felt reports
    - Returns data in requested format (JSON/XML)

    Returns: Filtered earthquake data including only events with specified minimum felt reports
    Used for: Analyzing earthquakes that were actually felt by SF Bay Area residents
"""

@router.get("/earthquake-felt")
def get_sf_earthquakes_felt(
    # Required parameters with descriptive error messages if missing
    start_time: str = Query(..., description="Start time (YYYY-MM-DDTHH:MM:SS)"),
    end_time: str = Query(..., description="End time (YYYY-MM-DDTHH:MM:SS)"),

    # Optional parameters with default values
    format: str = Query('json', description="Response format (json or xml)"),
    min_felt_reports: int = Query(10, description="Minimum felt reports"),
):
    
    # Validate that dates are in the correct format before processing
    start = validate_date(start_time, "Start_time")
    end = validate_date(end_time, "end_time")
    """Get earthquakes with minimum felt reports in SF Bay Area"""
    # Set up parameters for USGS API query
    params = {
        "format": "geojson",
        "starttime": start,
        "endtime": end,
        "minmagnitude": 2.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "maxradiuskm": 100
    }
    data = fetch_usgs_data(params)

        
    # Filter for felt reports
    felt_earthquakes = {
        "type": "FeatureCollection",
        "features": [
            # Filter features based on minimum felt reports
            # Only include if:
            # 1. The 'felt' property exists and isn't None
            # 2. The number of felt reports meets our minimum threshold
            feature for feature in data["features"]
            if feature["properties"].get("felt", 0) is not None 
            and int(feature["properties"].get("felt", 0)) >= min_felt_reports
        ]
    }
    # Return the filtered data in the requested format (JSON/XML)
    return format_response(felt_earthquakes, format)