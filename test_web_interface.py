#!/usr/bin/env python3
"""
Test script to verify the web interface and API are working properly
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints"""
    print("🔍 Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ API health check: PASSED")
        else:
            print(f"❌ API health check: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API health check: FAILED - {e}")
        return False
    
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
            print("✅ API prediction: PASSED")
            print(f"   Recommendation: {result.get('suggestion', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"❌ API prediction: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API prediction: FAILED - {e}")
        return False
    
    return True

def test_web_interface():
    """Test the web interface"""
    print("\n🌐 Testing web interface...")
    
    # Test web interface homepage
    try:
        response = requests.get("http://localhost:5002/", timeout=5)
        if response.status_code == 200:
            print("✅ Web interface homepage: PASSED")
        else:
            print(f"❌ Web interface homepage: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Web interface homepage: FAILED - {e}")
        return False
    
    # Test web interface API status endpoint
    try:
        response = requests.get("http://localhost:5002/api-status", timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('connected'):
                print("✅ Web interface API connection: PASSED")
            else:
                print("❌ Web interface API connection: FAILED - API not connected")
                return False
        else:
            print(f"❌ Web interface API status: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Web interface API status: FAILED - {e}")
        return False
    
    # Test web interface prediction endpoint
    test_data = {
        "temperature": 20,
        "humidity": 60,
        "wind_speed": 3
    }
    
    try:
        response = requests.post(
            "http://localhost:5002/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Web interface prediction: PASSED")
            print(f"   Recommendation: {result.get('suggestion', 'N/A')}")
        else:
            print(f"❌ Web interface prediction: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Web interface prediction: FAILED - {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Clothing Recommendation System - Web Interface Test")
    print("=" * 60)
    
    # Wait a moment for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(2)
    
    # Test API
    api_ok = test_api()
    
    if not api_ok:
        print("\n❌ API tests failed. Please make sure the API is running on port 5001")
        print("   Run: python app.py")
        return
    
    # Test web interface
    web_ok = test_web_interface()
    
    if not web_ok:
        print("\n❌ Web interface tests failed. Please check the web interface on port 5002")
        print("   Run: python web_interface.py")
        return
    
    print("\n🎉 All tests passed!")
    print("\n🌐 Your web interface should be working at: http://localhost:5002")
    print("📡 API is available at: http://localhost:5001")
    print("\n💡 If you're still having issues accessing the web page:")
    print("   1. Make sure both services are running")
    print("   2. Try accessing http://127.0.0.1:5002 instead of localhost")
    print("   3. Check your browser's developer console for any errors")
    print("   4. Try a different browser or incognito mode")

if __name__ == "__main__":
    main() 