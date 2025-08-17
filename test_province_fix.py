#!/usr/bin/env python3
"""
Test script để kiểm tra province mapping fix
"""

import requests
import json

# Test province mapping
test_cases = [
    {
        'name': 'Đồng Nai (short name)',
        'params': {
            'type': 'custom',
            'province': 'Đồng Nai',
            'gender': 'Nam,Nữ',
            'hasPhone': 'true'
        }
    },
    {
        'name': 'Tỉnh Đồng Nai (full name)', 
        'params': {
            'type': 'custom',
            'province': 'Tỉnh Đồng Nai',
            'gender': 'Nam,Nữ',
            'hasPhone': 'true'
        }
    },
    {
        'name': 'No filters',
        'params': {
            'type': 'all'
        }
    }
]

base_url = 'http://localhost:5000/api/export-count'

print("🧪 Testing province mapping fix...")
print("=" * 50)

for test in test_cases:
    print(f"\n📋 Test: {test['name']}")
    try:
        response = requests.get(base_url, params=test['params'])
        if response.ok:
            data = response.json()
            count = data.get('count', 0)
            print(f"✅ Count: {count}")
            print(f"🔗 URL: {response.url}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✨ Test completed!")
