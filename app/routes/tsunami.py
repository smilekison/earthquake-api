from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from app.utils import fetch_usgs_data, format_response, validate_date
from app.logger import setup_logging

logger = setup_logging()
router = APIRouter()

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
        # Parse start time
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        # Calculate end time by subtracting the time range in hours
        end_time = start_time - timedelta(hours=time_range)

        # Validate the date formats
        start = validate_date(start_time.isoformat(), "Start_time")
        end = validate_date(end_time.isoformat(), "End_time")

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
                feature for feature in data["features"]
                if feature["properties"].get("tsunami", 0) > 0
            ]
        }

        return format_response(tsunami_quakes, format)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format: {str(e)}"
        )
