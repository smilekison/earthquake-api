from fastapi import APIRouter, Query
from app.utils import fetch_usgs_data, format_response, validate_date

router = APIRouter()

@router.get("/earthquake/sf")
def get_sf_earthquakes(
    start_time: str = Query(..., description="Start time (YYYY-MM-DDTHH:MM:SS)"),
    end_time: str = Query(..., description="End time (YYYY-MM-DDTHH:MM:SS)"),
    format: str = Query('json', description="Response format (json or xml)"),
    min_magnitude: float = Query(2.0, description="Minimum magnitude")
):
    start = validate_date(start_time, "Start_time")
    end = validate_date(end_time, "end_time")
    params = {
        "format": "geojson",
        "starttime": start,
        "endtime": end,
        "minmagnitude": min_magnitude,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "maxradiuskm": 100
    }
    data = fetch_usgs_data(params)
    return format_response(data, format)
