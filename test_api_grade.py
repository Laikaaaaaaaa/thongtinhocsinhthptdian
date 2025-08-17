#!/usr/bin/env python3
"""
Test export-count API directly
"""

import requests
import json

def test_export_count_api():
    """Test export-count API directly"""
    base_url = 'http://localhost:5000/api/export-count'
    
    tests = [
        {
            'name': 'All students',
            'params': {'type': 'all'}
        },
        {
            'name': 'Grade 11',
            'params': {'type': 'grade', 'grade': '11'}
        },
        {
            'name': 'Grade 10', 
            'params': {'type': 'grade', 'grade': '10'}
        },
        {
            'name': 'Specific classes',
            'params': {'type': 'class', 'classes': '11A1,11A2'}
        }
    ]
    
    print("🧪 Testing export-count API...")
    print("=" * 50)
    
    for test in tests:
        print(f"\n📋 Test: {test['name']}")
        try:
            response = requests.get(base_url, params=test['params'], timeout=5)
            print(f"🔗 URL: {response.url}")
            
            if response.ok:
                data = response.json()
                count = data.get('count', 'N/A')
                print(f"✅ Status: {response.status_code}")
                print(f"📊 Count: {count}")
                if 'error' in data:
                    print(f"⚠️ Error in response: {data['error']}")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"❌ Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - server not running on localhost:5000")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    test_export_count_api()
