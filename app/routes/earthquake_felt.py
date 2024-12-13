from fastapi import APIRouter, Query
from app.utils import fetch_usgs_data, format_response, validate_date
from app.redis_client import get_redis_client


router = APIRouter()

@router.get("/earthquake-felt")
def get_sf_earthquakes_felt(
    start_time: str = Query(..., description="Start time (YYYY-MM-DDTHH:MM:SS)"),
    end_time: str = Query(..., description="End time (YYYY-MM-DDTHH:MM:SS)"),
    format: str = Query('json', description="Response format (json or xml)"),
    min_felt_reports: int = Query(10, description="Minimum felt reports"),
):
    start = validate_date(start_time, "Start_time")
    end = validate_date(end_time, "end_time")
    """Get earthquakes with minimum felt reports in SF Bay Area"""
    # Get base earthquake data
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
            feature for feature in data["features"]
            if feature["properties"].get("felt", 0) is not None 
            and int(feature["properties"].get("felt", 0)) >= min_felt_reports
        ]
    }
    
    return format_response(felt_earthquakes, format)