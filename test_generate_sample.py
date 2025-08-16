#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_generate_sample_data():
    url = "http://localhost:5000/api/generate-sample-data"
    
    data = {
        "count": 3
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🧪 Testing generate sample data API...")
        print(f"📡 URL: {url}")
        print(f"📦 Data: {data}")
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Success! Created {result.get('created_count')} students")
            else:
                print(f"❌ API returned error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running on http://localhost:5000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_generate_sample_data()
