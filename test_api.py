#!/usr/bin/env python3
"""
Simple test script for the Clothing Recommendation API

This script demonstrates how to use the API and tests various scenarios.
"""

import requests
import json
import time
import sys

# API base URL
BASE_URL = "http://localhost:5000"

def test_api_health():
    """Test the health endpoint."""
    print("🏥 Testing API health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy - Model status: {data.get('model_status', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running?")
        return False

def test_api_info():
    """Test the home endpoint."""
    print("\n📋 Testing API information...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Info: {data.get('message', 'Unknown')}")
            print(f"📡 Available endpoints: {list(data.get('endpoints', {}).keys())}")
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        return False

def test_single_prediction(weather_data):
    """Test a single prediction."""
    print(f"\n🔮 Testing prediction for: {weather_data}")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=weather_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction: {data['suggestion']}")
            print(f"🎯 Confidence: {data['confidence']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Error: {response.json().get('error', 'Unknown error')}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        return False

def test_batch_predictions(weather_conditions):
    """Test batch predictions."""
    print(f"\n📦 Testing batch predictions for {len(weather_conditions)} conditions...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json={'weather_conditions': weather_conditions},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch predictions completed: {data['count']} predictions")
            for pred in data['predictions']:
                print(f"  - {pred['weather_conditions']} → {pred['suggestion']} (confidence: {pred['confidence']})")
            return True
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            print(f"Error: {response.json().get('error', 'Unknown error')}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        return False

def test_error_handling():
    """Test error handling with invalid inputs."""
    print("\n🚨 Testing error handling...")
    
    # Test missing field
    print("Testing missing field...")
    invalid_data = {'temperature': 15, 'humidity': 50}  # Missing wind_speed
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    if response.status_code == 400:
        print("✅ Correctly handled missing field")
    else:
        print(f"❌ Unexpected response for missing field: {response.status_code}")
    
    # Test invalid temperature
    print("Testing invalid temperature...")
    invalid_data = {'temperature': 100, 'humidity': 50, 'wind_speed': 5}  # Too hot
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    if response.status_code == 400:
        print("✅ Correctly handled invalid temperature")
    else:
        print(f"❌ Unexpected response for invalid temperature: {response.status_code}")
    
    # Test invalid JSON
    print("Testing invalid JSON...")
    response = requests.post(
        f"{BASE_URL}/predict",
        data="invalid json",
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code == 400:
        print("✅ Correctly handled invalid JSON")
    else:
        print(f"❌ Unexpected response for invalid JSON: {response.status_code}")

def main():
    """Main test function."""
    print("🧪 Clothing Recommendation API Test Suite")
    print("=" * 50)
    
    # Wait a moment for API to be ready
    print("⏳ Waiting for API to be ready...")
    time.sleep(2)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not available. Please ensure:")
        print("   1. The model has been trained: python train_model.py")
        print("   2. The API is running: python app.py")
        print("   3. The API is accessible at http://localhost:5000")
        sys.exit(1)
    
    # Test API info
    test_api_info()
    
    # Test various weather scenarios
    test_cases = [
        {'temperature': 25, 'humidity': 60, 'wind_speed': 3},   # Should be T-shirt
        {'temperature': 15, 'humidity': 50, 'wind_speed': 5},   # Should be Light jacket
        {'temperature': 5, 'humidity': 80, 'wind_speed': 10},   # Should be Coat
        {'temperature': 30, 'humidity': 40, 'wind_speed': 2},   # Should be T-shirt
        {'temperature': 0, 'humidity': 90, 'wind_speed': 15},   # Should be Coat
    ]
    
    print("\n🌤️ Testing various weather scenarios:")
    for i, case in enumerate(test_cases, 1):
        test_single_prediction(case)
    
    # Test batch predictions
    batch_conditions = [
        {'temperature': 20, 'humidity': 55, 'wind_speed': 4},
        {'temperature': 10, 'humidity': 70, 'wind_speed': 8},
        {'temperature': -2, 'humidity': 85, 'wind_speed': 12},
    ]
    test_batch_predictions(batch_conditions)
    
    # Test error handling
    test_error_handling()
    
    print("\n🎉 All tests completed!")
    print("\n💡 You can now use the API with:")
    print("   curl -X POST http://localhost:5000/predict \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"temperature\": 15, \"humidity\": 50, \"wind_speed\": 5}'")

if __name__ == "__main__":
    main() 