# This file contains helpful tools we use throughout our earthquake service

from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from datetime import datetime
import requests
import json
import xmltodict
from app.config import USGS_API_URL, CACHE_DURATION
from app.redis_client import redis_client
from app.logger import setup_logging

# Start logging the information
logger = setup_logging()


"""
def validate_date(date_str: str, param_name: str = "date") -> str:
    Purpose: Validates date strings to ensure they match required format
    What it does:
    - Takes a date string and parameter name as input
    - Checks if date matches format: YYYY-MM-DDTHH:MM:SS
    - Raises exception with message if format is invalid
    Parameters:
    - date_str: The date string to validate
    - param_name: Name of the parameter (for error messages)
    Returns: The validated date string
    Used for: Ensuring date inputs for earthquake queries are properly formatted
"""
def validate_date(date_str: str, param_name: str = "date") -> str:
    
    # Check if a date string is written in correct format (like "2014-01-01T00:00:00")
    try:
        datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        return date_str
    except ValueError:
    # Raise exception error, date not properly formatted.
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {param_name}. Please use format: YYYY-MM-DDTHH:MM:SS (example: 2014-01-01T00:00:00)"
        )


"""
def fetch_usgs_data(params: dict) -> dict:

    Purpose: Retrieves earthquake data from USGS API with caching
    What it does:
    - Checks Redis cache for existing data
    - If cached data exists, returns it
    - If no cached data, fetches from USGS API
    - Stores new data in cache for future use
    - Handles errors in API communication
    Parameters:
    - params: Dictionary of query parameters for USGS API
    Returns: Dictionary containing earthquake data
    Used for: Getting earthquake information while minimizing API calls
"""

def fetch_usgs_data(params: dict) -> dict:
    # Get earthquake data from USGS, but first check if we already have it as cache in Redis server.
    try:
        # Make sure all our search terms are text strings
        clean_params = {k: str(v) for k, v in params.items()}
        # Create a special label for this specific search
        cache_key = f"usgs_data:{json.dumps(clean_params, sort_keys=True)}"

        # If we have our notepad (Redis) working:
        if redis_client:
            # Check if we already wrote down this information
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info("🎯 Cache HIT: Returning cached data")
                return json.loads(cached_data)
            logger.info("❌ Cache MISS: Fetching from USGS API")
        # If we didn't find it in our notes, ask USGS
        response = requests.get(USGS_API_URL, params=clean_params)
        response.raise_for_status()
        data = response.json()


        # If our notepad is working, write down this new information
        if redis_client:
            redis_client.setex(cache_key, CACHE_DURATION, json.dumps(data))
            logger.info("💾 Stored new data in cache")
            
        return data
    except Exception as e:
        # If anything goes wrong, write it in our diary and tell the user
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Error fetching data: {str(e)}")



"""
def format_response(data: dict, format_type: str = 'json'):
    
    Purpose: Converts API response to requested format (JSON or XML)
    What it does:
    - Takes data and desired format type as input
    - Converts data to XML if requested
    - Returns JSON by default
    Parameters:
    - data: Dictionary containing response data
    - format_type: Desired format ('json' or 'xml')
    Returns: Formatted response in specified format
    Used for: Providing data in user's preferred format
"""
def format_response(data: dict, format_type: str = 'json'):
    #  Package our earthquake data in the format the user wants (JSON or XML)
    if format_type.lower() == 'xml':
        # If they want XML, convert our data to XML format
        xml_data = xmltodict.unparse({"response": data}, pretty=True)
        return Response(content=xml_data, media_type="application/xml")
    # Otherwise, give them JSON (this is like our default wrapping paper)
    return JSONResponse(content=data)
