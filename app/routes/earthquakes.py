from fastapi import APIRouter, Query
from app.utils import fetch_usgs_data, format_response, validate_date

router = APIRouter()

"""
    Purpose: Retrieves all earthquakes in the SF Bay Area within specified parameters
    
    What it does:
    - Validates input date parameters
    - Fetches earthquake data within 100km radius of San Francisco
    - Filters based on minimum magnitude
    - Returns data in requested format (JSON/XML)
    
    Parameters:
    - start_time: Start of time range (YYYY-MM-DDTHH:MM:SS)
    - end_time: End of time range (YYYY-MM-DDTHH:MM:SS)
    - format: Response format ('json' or 'xml')
    - min_magnitude: Minimum earthquake magnitude to include
    
    Returns: Filtered earthquake data for SF Bay Area
    Used for: Getting general earthquake activity around San Francisco
"""

@router.get("/earthquake/sf")
def get_sf_earthquakes(
    # Define required and optional query parameters with descriptions
    start_time: str = Query(..., description="Start time (YYYY-MM-DDTHH:MM:SS)"),
    end_time: str = Query(..., description="End time (YYYY-MM-DDTHH:MM:SS)"),
    format: str = Query('json', description="Response format (json or xml)"),
    min_magnitude: float = Query(2.0, description="Minimum magnitude")
):
    
    # Validate date formats before processing
    start = validate_date(start_time, "Start_time")
    end = validate_date(end_time, "end_time")
    params = {
        "format": "geojson",               # Request GeoJSON formatted data
        "starttime": start,                # Start of time window
        "endtime": end,                    # End of time window
        "minmagnitude": min_magnitude,     # Minimum earthquake magnitude to include
        "latitude": 37.7749,              # SF latitude
        "longitude": -122.4194,           # SF longitude
        "maxradiuskm": 100                # Search radius in kilometers
    }

    # Get earthquake data and return in requested format
    data = fetch_usgs_data(params)
    return format_response(data, format)
