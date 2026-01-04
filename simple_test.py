#!/usr/bin/env python3
"""
Simple test script for the Commute Estimation API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def main():
    print("🧪 Simple Commute API Test")
    print("="*60)

    # Test 1: Root endpoint
    print("\n1️⃣  Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)

    # Test 2: Health check
    print("\n2️⃣  Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)

    # Test 3: Calculate routes
    print("\n3️⃣  Testing route calculation...")
    route_data = {
        "origin": "612 N St Asaph St, Alexandria, VA 22314",
        "destination": "1850 N Moore St, Arlington, VA 22209"
        # "arrival_time": "2026-01-28T12:00:00Z"
    }
    print(f"Request: {json.dumps(route_data, indent=2)}")

    response = requests.post(f"{BASE_URL}/routes", json=route_data)
    print_response("Route Calculation", response)

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            routes_count = len(result.get("routes", []))
            print(f"\n✅ Success! Found {routes_count} route(s)")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
    else:
        print("/routes test request failed")
        return -1

    # Test 4: Calculate routes with formatted output
    print("\n4️⃣  Testing formatted route calculation...")
    response = requests.post(f"{BASE_URL}/routes/formatted", json=route_data)
    print_response("Formatted Route Calculation", response)
    if(response.status_code != 200):
        print("/routes/formatted test request failed")
        return -1

    print("\n" + "="*60)
    print("✅ Tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python api.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
