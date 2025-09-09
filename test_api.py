#!/usr/bin/env python3
"""
Test script for the Clarifai Image Analysis API
Run this after deployment to verify everything works
"""

import requests
import json

# Update this URL after deployment
BASE_URL = "https://your-app-name.railway.app"  # Replace with actual Railway URL
API_TOKEN = "xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_docs():
    """Test the docs endpoint"""
    print("\nTesting docs endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Status: {response.status_code}")
        print("Docs available at:", f"{BASE_URL}/docs")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_auth():
    """Test authentication"""
    print("\nTesting authentication...")
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        # This will fail with 422 because no file is provided, but should not be 401
        response = requests.post(f"{BASE_URL}/analyze-image", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("❌ Authentication failed")
            return False
        else:
            print("✅ Authentication working (expected 422 for missing file)")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("🚀 Testing Clarifai Image Analysis API")
    print("=" * 50)
    
    # Update the BASE_URL first
    if "your-app-name" in BASE_URL:
        print("⚠️  Please update BASE_URL in this script with your actual Railway URL")
        print("   Example: https://clarifai-api-production.railway.app")
        return
    
    tests = [
        ("Health Check", test_health),
        ("API Documentation", test_docs),
        ("Authentication", test_auth)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed! API is ready for use.")
    else:
        print("\n⚠️  Some tests failed. Check the deployment.")

if __name__ == "__main__":
    main()
