#!/usr/bin/env python3
"""
Test script to verify the web interface works in container environment
"""

import requests
import json
import time

def test_container_web():
    """Test the web interface in container environment"""
    print("🧪 Testing Container Web Interface")
    print("=" * 50)
    
    # Test the root endpoint (should serve HTML)
    print("🔍 Testing root endpoint (should serve HTML)...")
    try:
        response = requests.get("http://localhost:5001/", timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'text/html' in content_type:
                print("✅ Root endpoint serves HTML correctly")
                print(f"   Content-Type: {content_type}")
                print(f"   Content length: {len(response.text)} characters")
                
                # Check if it contains expected HTML elements
                if '<title>👕 Clothing Recommendation System</title>' in response.text:
                    print("✅ HTML contains expected title")
                else:
                    print("⚠️  HTML might not be the expected content")
                    
            else:
                print("❌ Root endpoint doesn't serve HTML")
                print(f"   Content-Type: {content_type}")
                print("   This means you're still getting the API JSON response")
                
        else:
            print(f"❌ Root endpoint failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Root endpoint test failed: {e}")
    
    print("\n🔍 Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint works")
        else:
            print(f"❌ Health endpoint failed (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    # Test prediction endpoint
    test_data = {
        "temperature": 15,
        "humidity": 50,
        "wind_speed": 5
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction endpoint works")
            print(f"   Recommendation: {result.get('suggestion', 'N/A')}")
        else:
            print(f"❌ Prediction endpoint failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Prediction endpoint test failed: {e}")
    
    print("\n🌐 Web Interface Instructions:")
    print("=" * 50)
    print("1. Open your browser and go to: http://localhost:5001")
    print("2. You should see a beautiful web interface with:")
    print("   - Temperature, humidity, and wind speed input fields")
    print("   - Quick example buttons")
    print("   - API connection status")
    print("3. Enter weather data and click 'Get Recommendation'")
    print("4. You should see clothing recommendations with confidence scores")
    
    print("\n🔧 If you're still seeing JSON instead of HTML:")
    print("1. Make sure the 'static/index.html' file exists")
    print("2. Restart your container")
    print("3. Check container logs for any errors")
    print("4. Try accessing http://127.0.0.1:5001 instead of localhost")

if __name__ == "__main__":
    test_container_web() 