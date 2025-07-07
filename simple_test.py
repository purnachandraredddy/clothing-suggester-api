#!/usr/bin/env python3
"""
Simple test script for the Clothing Recommendation API
This script makes API calls and displays results in a user-friendly format.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5001"

def print_separator():
    """Print a separator line."""
    print("=" * 60)

def test_api_info():
    """Test and display API information."""
    print("📋 API Information:")
    print_separator()
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"🎯 API: {data['message']}")
            print(f"📦 Version: {data['version']}")
            print("\n📡 Available Endpoints:")
            for endpoint, description in data['endpoints'].items():
                print(f"   {endpoint} - {description}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_health():
    """Test and display health status."""
    print("\n🏥 Health Check:")
    print_separator()
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"🤖 Model Status: {data['model_status']}")
            print(f"📅 Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_prediction(weather_data, description=""):
    """Test a prediction and display results."""
    print(f"\n🔮 Prediction Test {description}:")
    print_separator()
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=weather_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"🌤️ Weather Conditions:")
            print(f"   Temperature: {data['weather_conditions']['temperature']}°C")
            print(f"   Humidity: {data['weather_conditions']['humidity']}%")
            print(f"   Wind Speed: {data['weather_conditions']['wind_speed']} km/h")
            
            print(f"\n👕 Recommendation:")
            print(f"   Clothing: {data['suggestion']}")
            print(f"   Confidence: {data['confidence']:.1%}")
            print(f"   Timestamp: {data['timestamp']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Message: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def main():
    """Main test function."""
    print("🧪 Clothing Recommendation API - Simple Test")
    print("=" * 60)
    
    # Test API information
    test_api_info()
    
    # Test health
    test_health()
    
    # Test various weather scenarios
    test_cases = [
        (
            {"temperature": 25, "humidity": 60, "wind_speed": 3},
            "(Hot Weather - Should suggest T-shirt)"
        ),
        (
            {"temperature": 15, "humidity": 50, "wind_speed": 5},
            "(Mild Weather - Should suggest Light jacket)"
        ),
        (
            {"temperature": 5, "humidity": 80, "wind_speed": 10},
            "(Cold Weather - Should suggest Coat)"
        ),
        (
            {"temperature": 30, "humidity": 40, "wind_speed": 2},
            "(Very Hot Weather - Should suggest T-shirt)"
        ),
        (
            {"temperature": -2, "humidity": 90, "wind_speed": 15},
            "(Very Cold Weather - Should suggest Coat)"
        )
    ]
    
    for weather_data, description in test_cases:
        test_prediction(weather_data, description)
    
    print("\n🎉 All tests completed!")
    print("\n💡 You can also test manually with:")
    print("   curl -X POST http://localhost:5001/predict \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"temperature\": 15, \"humidity\": 50, \"wind_speed\": 5}' | python3 -m json.tool")

if __name__ == "__main__":
    main() 