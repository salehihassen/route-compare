#!/usr/bin/env python3
"""
Commute Time Calculator using Google Maps Routes API v2 (with PESSIMISTIC traffic model)

Usage:
  python commute.py "612 N St Asaph St, Alexandria, VA 22314" "1850 N Moore St, Arlington, VA 22209"
  python commute.py "origin" "destination" --arrival-time "2026-01-28T14:00:00Z"
"""

import json
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")
API_KEY = os.getenv("GMAPS_API_KEY")
ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def compute_routes(
    origin: str,
    destination: str,
    departure_time: Optional[str] = None,
    arrival_time: Optional[str] = None,
) -> dict:
    """
    Call Google Routes API v2 with PESSIMISTIC (worst-case) traffic model.
    """

    # Use arrival time if provided, otherwise departure time
    if arrival_time:
        time_field = "arrivalTime"
        time_value = arrival_time
    elif departure_time:
        time_field = "departureTime"
        time_value = departure_time
    else:
        time_field = "departureTime"
        time_value = datetime.utcnow().isoformat() + "Z"

    # Build the Routes API v2 request body
    request_body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "computeAlternativeRoutes": True,
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "trafficModel": "PESSIMISTIC",
        "polylineQuality": "OVERVIEW",
    }

    # Add time constraint (must be in RFC 3339 format)
    if time_field == "departureTime":
        request_body["departureTime"] = time_value
    elif time_field == "arrivalTime":
        request_body["arrivalTime"] = time_value

    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "*",
        "Content-Type": "application/json",
    }

    try:
        # print("DEBUG - Request body:", json.dumps(request_body, indent=2))
        response = requests.post(ROUTES_API_URL, json=request_body, headers=headers, timeout=10)
        # print("DEBUG - Response status:", response.status_code)
        # print("DEBUG - Response body:", response.text)

        response.raise_for_status()
        data = response.json()

        if "routes" not in data or not data["routes"]:
            return {"error": "No routes found"}

        return {
            "success": True,
            "time_field": time_field,
            "time_value": time_value,
            "routes": data.get("routes", []),
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}

def calculate_departure_time(arrival_time_iso: str, duration_seconds: int,
    timezone= "America/New_York") -> str:
    """Calculate the departure time given arrival time and duration."""
    arrival = datetime.fromisoformat(arrival_time_iso.replace('Z', '+00:00'))
    departure_utc = arrival - timedelta(seconds=duration_seconds)
    departure_local = departure_utc.astimezone(ZoneInfo(timezone))

    return departure_local.strftime("%I:%M %p").lstrip("0")

def format_duration(seconds: float) -> str:
    """Convert seconds (int or float) to human-readable duration string."""
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:  # Show seconds if no hours/minutes, or if there are seconds
        parts.append(f"{secs}s")

    return " ".join(parts)

def format_route_output(result: dict) -> str:
    """Format route results as human-readable text for Routes API v2."""

    if "error" in result:
        return f"❌ Error: {result['error']}"

    if not result.get("success"):
        return "❌ Failed to compute routes"

    output = []
    routes = result.get("routes", [])
    time_field = result.get("time_field", "departureTime")
    time_value = result.get("time_value", "")

    output.append(f"📍 Routes ({len(routes)} found) - PESSIMISTIC traffic model")
    output.append(f"   Reference: {time_field} = {time_value}")
    output.append("")

    for i, route in enumerate(routes, 1):
        output.append(f"Route {i}:")

        # Distance
        distance_m = route.get("distanceMeters", 0)
        distance_km = distance_m / 1000
        output.append(f"  Distance: {distance_km:.1f} km ({distance_m}m)")

        # Duration (PESSIMISTIC worst-case)
        duration_str = route["duration"] # in seconds
        duration_sec = float(duration_str[:].replace("s", ""))

        output.append(f"  Duration (PESSIMISTIC, Typical Worst Case): {format_duration(duration_sec)}")

            # Calculate departure time if arrival was specified
        if time_field == "arrivalTime":
            departure = calculate_departure_time(time_value, duration_sec)
            output.append(f"  Latest Departure (to arrive on time): {departure}")

        # Summary
        summary = route.get("summary", "")
        if summary:
            output.append(f"  Route: {summary}")

        # Polyline (for drawing on map)
        polyline = route.get("polyline", {})
        encoded = polyline.get("encodedPolyline", "")
        if encoded:
            output.append(f"  Polyline (encoded): {encoded[:60]}...")

        # Legs (segments of the route)
        legs = route.get("legs", [])
        # output.append(f"    Duration: {route_duration}")
        for leg_idx, leg in enumerate(legs, 1):
            output.append(f"  Leg {leg_idx}:")

            # Steps (turn-by-turn directions) - first 3 only
            steps = leg.get("steps", [])
            if steps:
                output.append(f"    Directions (first 3 steps):")
                for step_idx, step in enumerate(steps[:3], 1):
                    nav = step.get("navigationInstruction", {})
                    instruction = nav.get("instructions", "")
                    maneuver = nav.get("maneuver", "STRAIGHT")
                    if instruction:
                        output.append(f"      {step_idx}. {maneuver}: {instruction[:60]}")
                if len(steps) > 3:
                    output.append(f"      ... and {len(steps) - 3} more steps")

        output.append("")

    return "\n".join(output)



def main():
    parser = argparse.ArgumentParser(
        description="Calculate commute time with PESSIMISTIC (worst-case) traffic estimates using Routes API v2"
    )
    parser.add_argument("origin", help="Starting address")
    parser.add_argument("destination", help="Destination address")
    parser.add_argument("--depart-time", type=str, help="Departure time (ISO 8601, e.g., 2026-01-28T08:00:00Z)")
    parser.add_argument("--arrival-time", type=str, help="Arrival time (ISO 8601, e.g., 2026-01-28T14:00:00Z)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    result = compute_routes(
        origin=args.origin,
        destination=args.destination,
        departure_time=args.depart_time,
        arrival_time=args.arrival_time,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_route_output(result))


if __name__ == "__main__":
    main()
