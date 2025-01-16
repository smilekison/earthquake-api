from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from app.utils import fetch_usgs_data, format_response, validate_date
from app.logger import setup_logging

logger = setup_logging()
router = APIRouter()

"""
    Purpose: Retrieves earthquake events that triggered tsunami alerts for a specific US state
    
    What it does:
    - Validates and processes input date parameters
    - Calculates time range based on input hours
    - Fetches earthquake data from USGS
    - Filters for events with tsunami potential
    - Adds state-specific metadata to response
    
    Parameters:
    - state: US state to get alerts for
    - start_time: Start of time range (YYYY-MM-DDTHH:MM:SS)
    - time_range: Number of hours to look back (1-168)
    - format: Response format ('json' or 'xml')
    
    Returns: Filtered earthquake data showing only events with tsunami alerts
    
    Error Handling:
    - Validates date formats
    - Logs data fetching operations
    - Handles invalid input errors
    
    Used for: Monitoring tsunami risks from earthquakes in specific states
    """
@router.get("/{state}")
def get_tsunami_alerts(
    state: str,
    start_time: str = Query(..., description="Start time (YYYY-MM-DDTHH:MM:SS)"),
    time_range: int = Query(24, ge=1, le=168, description="Time range in hours (max 168)"),
    format: str = Query('json', description="Response format (json or xml)")
):
    """
    Get earthquakes with tsunami alerts for a US state starting from a specific time
    going back by the specified number of hours.
    """
    try:
        # Convert start time string to datetime object
        # Remove 'Z' suffix and add UTC timezone (+00:00)

        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        
        
        # Calculate end time by subtracting the time range in hours
        end_time = start_time - timedelta(hours=time_range)

        # Validate both date strings are in correct format
        start = validate_date(start_time.isoformat(), "Start_time")
        end = validate_date(end_time.isoformat(), "End_time")

        # Printing for more information for debugging purpose
        logger.info(f"Fetching tsunami data from {end} to {start}")

        # Fetch data from USGS API
        data = fetch_usgs_data({
            "format": "geojson",
            "starttime": end,
            "endtime": start,
            "minmagnitude": 2.0
        })

        # Filter for tsunami-related earthquakes
        tsunami_quakes = {
            "type": "FeatureCollection",
            "metadata": {
                "state": state,
                "time_range": f"{time_range} hours",
                "start_time": start,
                "end_time": end
            },
            "features": [

                # Only include earthquakes that triggered tsunami alerts
                # tsunami property > 0 indicates a tsunami alert was issued
                feature for feature in data["features"]
                if feature["properties"].get("tsunami", 0) > 0
            ]
        }

        return format_response(tsunami_quakes, format)

    except ValueError as e:
        # Handle invalid date format errors with clear error message
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format: {str(e)}"
        )
