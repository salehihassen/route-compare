# Simple Commute Estimation API

A minimal FastAPI wrapper for the commute estimation functions with debug logging.

## Features


## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp EXAMPLE.env .env
# Edit .env and add your Google Maps API key
```

## Running the API

Start the server:
```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Root Endpoint
```bash
GET /
```
Returns API information and available endpoints.

### Health Check
```bash
GET /health
```
Returns health status and API configuration.

### Calculate Routes
```bash
POST /routes
Content-Type: application/json

{
  "origin": "612 N St Asaph St, Alexandria, VA 22314",
  "destination": "1850 N Moore St, Arlington, VA 22209",
  "departure_time": "2024-01-15T08:00:00Z"
}
```

### Calculate Routes (Formatted)
```bash
POST /routes/formatted
Content-Type: application/json

{
  "origin": "612 N St Asaph St, Alexandria, VA 22314",
  "destination": "1850 N Moore St, Arlington, VA 22209"
}
```
Returns both formatted text and raw JSON data.

## Testing

Run the simple test script:
```bash
python simple_test.py
```

## Debug Logging

The API logs detailed information to:
- Console output
- `api_debug.log` file

Logs include:
- Startup information
- API key configuration status
- Request details
- Function call traces
- Error details with stack traces

## Example Usage

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Calculate routes
curl -X POST http://localhost:8000/routes \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "612 N St Asaph St, Alexandria, VA 22314",
    "destination": "1850 N Moore St, Arlington, VA 22209"
  }'
```

### Using Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Calculate routes
route_data = {
    "origin": "612 N St Asaph St, Alexandria, VA 22314",
    "destination": "1850 N Moore St, Arlington, VA 22209"
}

response = requests.post(f"{BASE_URL}/routes", json=route_data)
result = response.json()

if result.get("success"):
    print(f"Found {len(result['routes'])} route(s)")
    for i, route in enumerate(result['routes'], 1):
        print(f"Route {i}: {route.get('summary', 'Unknown')}")
else:
    print(f"Error: {result.get('error')}")
```

## Troubleshooting

### API won't start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Check that `commute.py` exists in the same directory
- Check the console output for error messages

### Routes return errors
- Check that your Google Maps API key is set in `.env`
- Check that the API key has the Routes API enabled
- Check `api_debug.log` for detailed error information
- Verify your addresses are valid

### Can't connect to API
- Make sure the server is running: `python api.py`
- Check that it's running on port 8000
- Try accessing `http://localhost:8000/docs` in your browser

## Project Structure

```
estimate-commute/
├── api.py              # Main FastAPI application
├── commute.py          # Google Maps route calculation functions
├── simple_test.py      # Test script
├── requirements.txt    # Python dependencies
├── EXAMPLE.env         # Environment variables template
├── .env                # Your environment variables (create this)
└── api_debug.log       # Debug log file (auto-generated)
```

## Notes

- No authentication required - perfect for testing and development
- No database - all state is managed in memory
- Debug logging helps troubleshoot issues quickly
- CORS enabled for easy frontend integration
