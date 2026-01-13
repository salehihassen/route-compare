#!/usr/bin/env python3
"""
Simple FastAPI wrapper for commute estimation functions
No authentication, no database, just clean API with debug logging
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import datetime as dt
import sys
import os

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler('api_debug.log')
    ]
)

logger = logging.getLogger(__name__)

# Import commute functions
try:
    from commute import compute_routes, format_route_output
    logger.info("✅ Successfully imported commute functions")
except ImportError as e:
    logger.error(f"❌ Failed to import commute functions: {e}")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Commute Estimation API",
    description="Simple API for estimating commute times using Google Maps Routes API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class RouteRequest(BaseModel):
    """Model for route calculation request"""
    origin: str
    destination: str
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("="*60)
    logger.info("🚀 Commute API Starting...")
    logger.info("="*60)
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")

    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        logger.info(f"✅ .env file found at {os.path.abspath(env_file)}")
    else:
        logger.warning(f"⚠️  .env file not found at {os.path.abspath(env_file)}")

    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GMAPS_API_KEY")
    if api_key:
        logger.info(f"✅ GMAPS_API_KEY is set (length: {len(api_key)})")
    else:
        logger.error("❌ GMAPS_API_KEY is not set in environment variables")

    logger.info("="*60)
    logger.info("✅ Commute API started successfully!")
    logger.info("📚 API Documentation: http://localhost:8000/docs")
    logger.info("="*60)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    logger.info("📡 Root endpoint called")
    return {
        "message": "Commute Estimation API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "routes": "/routes",
            "health": "/health"
        },
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("🏥 Health check called")

    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GMAPS_API_KEY")

    health_status = {
        "status": "healthy",
        "service": "commute-api",
        "timestamp":  dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_key_configured": api_key is not None
    }

    logger.info(f"Health status: {health_status}")
    return health_status


@app.post("/routes")
async def calculate_routes(request: RouteRequest):
    """
    Calculate routes between origin and destination

    - **origin**: Starting address
    - **destination**: Destination address
    - **departure_time**: Optional departure time (ISO 8601 format)
    - **arrival_time**: Optional arrival time (ISO 8601 format)

    Note: Only one of departure_time or arrival_time should be provided.
    """
    logger.info("="*60)
    logger.info("🚗 Route calculation requested")
    logger.info(f"Origin: {request.origin}")
    logger.info(f"Destination: {request.destination}")
    logger.info(f"Departure time: {request.departure_time}")
    logger.info(f"Arrival time: {request.arrival_time}")
    logger.info("="*60)

    try:
        # Call the compute_routes function
        logger.debug("Calling compute_routes function...")
        result = compute_routes(
            origin=request.origin,
            destination=request.destination,
            departure_time=request.departure_time,
            arrival_time=request.arrival_time
        )

        logger.debug(f"compute_routes returned: {type(result)}")

        # Check for errors in the result
        if "error" in result:
            logger.error(f"❌ Error in route calculation: {result['error']}")
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )

        if not result.get("success"):
            logger.error("❌ Route calculation failed")
            raise HTTPException(
                status_code=500,
                detail="Failed to compute routes"
            )

        # Log success information
        routes_count = len(result.get("routes", []))
        logger.info(f"✅ Successfully computed {routes_count} route(s)")
        logger.info(f"Time field: {result.get('time_field')}")
        logger.info(f"Time value: {result.get('time_value')}")

        # Add metadata to response
        result["api_metadata"] = {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "routes_count": routes_count,
            "request_params": {
                "origin": request.origin,
                "destination": request.destination,
                "has_departure_time": request.departure_time is not None,
                "has_arrival_time": request.arrival_time is not None
            }
        }

        logger.info("="*60)
        logger.info("✅ Route calculation completed successfully")
        logger.info("="*60)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in route calculation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/routes/formatted")
async def calculate_routes_formatted(request: RouteRequest):
    """
    Calculate routes and return formatted text output

    Same as /routes but returns human-readable text instead of JSON
    """
    logger.info("📝 Formatted route calculation requested")

    try:
        result = compute_routes(
            origin=request.origin,
            destination=request.destination,
            departure_time=request.departure_time,
            arrival_time=request.arrival_time
        )

        formatted_output = format_route_output(result)

        return {
            "formatted_text": formatted_output,
            "raw_data": result,
            "timestamp":  dt.datetime.now(dt.timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error in formatted route calculation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting server with uvicorn...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
    )
