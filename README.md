# Earthquake API Service

A FastAPI-based service that provides earthquake data for the San Francisco Bay Area. The service includes endpoints for general earthquake information, felt earthquakes, and tsunami alerts.

## Features

- 🌎 Get earthquake data for SF Bay Area
- 👥 Filter earthquakes by number of felt reports
- 🌊 Get tsunami alerts by state
- 💾 Redis caching for improved performance
- 🔄 Support for both JSON and XML response formats

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher (if running locally)
- Redis (handled by Docker Compose)

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository>
```

2. Start the services:
```bash
docker build -t earthquake-api .

docker-compose up -d
```

The API will be available at http://localhost:8000

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis (ensure Redis is installed locally):
```bash
redis-server
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Earthquakes in SF Bay Area
```http
GET /earthquake/sf
```
Parameters:
- `start_time`: Start time (YYYY-MM-DDTHH:MM:SS)
- `end_time`: End time (YYYY-MM-DDTHH:MM:SS)
- `format`: Response format (json or xml)
- `min_magnitude`: Minimum magnitude (default: 2.0)

### Felt Earthquakes
```http
GET /earthquake-felt
```
Parameters:
- `start_time`: Start time (YYYY-MM-DDTHH:MM:SS)
- `end_time`: End time (YYYY-MM-DDTHH:MM:SS)
- `format`: Response format (json or xml)
- `min_felt_reports`: Minimum number of felt reports (default: 10)

### Tsunami Alerts
```http
GET /{state}
```
Parameters:
- `state`: US state code
- `start_time`: Start time (YYYY-MM-DDTHH:MM:SS)
- `time_range`: Time range in hours (1-168, default: 24)
- `format`: Response format (json or xml)

### Health Check
```http
GET /
```
Returns service health status and Redis connection state.

## Example Requests

### Get Recent Earthquakes
```bash
curl "http://localhost:8000/earthquake/sf?start_time=2024-01-01T00:00:00&end_time=2024-01-02T00:00:00"
```

### Get Felt Earthquakes
```bash
curl "http://localhost:8000/earthquake-felt?start_time=2024-01-01T00:00:00&end_time=2024-01-02T00:00:00&min_felt_reports=20"
```

### Get Tsunami Alerts
```bash
curl "http://localhost:8000/CA?start_time=2024-01-01T00:00:00&time_range=48"
```

## Project Structure

```
earthquake-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── redis_client.py
│   ├── utils.py
│   └── routes/
│       ├── earthquakes.py
│       ├── earthquake_felt.py
│       ├── tsunami.py
│       └── health.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Environment Variables

- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)

## Development

To run the application in development mode:
```bash
docker-compose up --build
```

The `--reload` flag is enabled in development for automatic reloading on code changes.

## Data Source

This service uses the USGS Earthquake API for earthquake data. The data is cached in Redis to improve performance and reduce API calls.

## Cache Duration

Earthquake data is cached for 30 seconds to balance between data freshness and API performance.
