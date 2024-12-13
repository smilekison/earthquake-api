import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CACHE_DURATION = 30  # seconds
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
