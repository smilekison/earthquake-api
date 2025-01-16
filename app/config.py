'''
Configuration module for the Earthquake API Service
Contains environment variables and constants used throughout the application
Manages Redis connection settings and USGS API endpoint configuration
'''

import os
# Where to find our Redis database - if not specified, use 'localhost' (our own computer)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# Searth REDIS_PORT in .env file or if not found use 6379 as default port.
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# How long to remember (cache) our earthquake data - 30 seconds
CACHE_DURATION = 30  # seconds

# The web address where we can get earthquake information from USGS
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"