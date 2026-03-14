#!/usr/bin/env python3
"""
Test script for the exploit analysis API.
Run this to verify the endpoint works correctly.
"""
import requests
import json

# Read the exploit text
with open('test_euler_clean.txt', 'r') as f:
    exploit_text = f.read().strip()

# Prepare the request
url = "http://localhost:8001/analyze-exploit"
payload = {
    "exploit_text": exploit_text
}

print("Testing /analyze-exploit endpoint...")
print(f"URL: {url}")
print(f"Payload length: {len(exploit_text)} characters")
print("\nSending request...\n")

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success! Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"\n❌ Error: {response.status_code}")
        print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to server.")
    print("Make sure the server is running on port 8001:")
    print("  uvicorn app.main:app --reload --port 8001")
except Exception as e:
    print(f"❌ Error: {e}")
