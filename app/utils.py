from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from datetime import datetime
import requests
import json
import xmltodict
from app.config import USGS_API_URL, CACHE_DURATION
from app.redis_client import redis_client
from app.logger import setup_logging

logger = setup_logging()

def validate_date(date_str: str, param_name: str = "date") -> str:
    try:
        datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        return date_str
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {param_name}. Please use format: YYYY-MM-DDTHH:MM:SS (example: 2014-01-01T00:00:00)"
        )

def fetch_usgs_data(params: dict) -> dict:
    try:
        clean_params = {k: str(v) for k, v in params.items()}
        cache_key = f"usgs_data:{json.dumps(clean_params, sort_keys=True)}"
        
        if redis_client:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info("🎯 Cache HIT: Returning cached data")
                return json.loads(cached_data)
            logger.info("❌ Cache MISS: Fetching from USGS API")
        
        response = requests.get(USGS_API_URL, params=clean_params)
        response.raise_for_status()
        data = response.json()
        
        if redis_client:
            redis_client.setex(cache_key, CACHE_DURATION, json.dumps(data))
            logger.info("💾 Stored new data in cache")
            
        return data
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Error fetching data: {str(e)}")

def format_response(data: dict, format_type: str = 'json'):
    if format_type.lower() == 'xml':
        xml_data = xmltodict.unparse({"response": data}, pretty=True)
        return Response(content=xml_data, media_type="application/xml")
    return JSONResponse(content=data)
