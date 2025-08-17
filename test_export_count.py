#!/usr/bin/env python3
"""
Test export-count function trực tiếp từ app
"""

from app import app
import json

def test_export_count_directly():
    print("🧪 Testing export-count function directly...")
    
    with app.test_client() as client:
        
        # Test 1: All students
        print("\n1️⃣ Test: All students")
        response = client.get('/api/export-count?type=all')
        data = response.get_json()
        print(f"   Result: {data}")
        
        # Test 2: Custom with no filters
        print("\n2️⃣ Test: Custom with no filters")
        response = client.get('/api/export-count?type=custom')
        data = response.get_json()
        print(f"   Result: {data}")
        
        # Test 3: Custom with Đồng Nai
        print("\n3️⃣ Test: Custom with Đồng Nai")
        response = client.get('/api/export-count?type=custom&province=Đồng Nai')
        data = response.get_json()
        print(f"   Result: {data}")
        
        # Test 4: Custom with gender
        print("\n4️⃣ Test: Custom with gender")
        response = client.get('/api/export-count?type=custom&gender=Nam,Nữ')
        data = response.get_json()
        print(f"   Result: {data}")
        
        # Test 5: Custom with phone
        print("\n5️⃣ Test: Custom with phone")
        response = client.get('/api/export-count?type=custom&hasPhone=true')
        data = response.get_json()
        print(f"   Result: {data}")
        
        # Test 6: Custom with all filters
        print("\n6️⃣ Test: Custom with all filters")
        response = client.get('/api/export-count?type=custom&province=Đồng Nai&gender=Nam,Nữ&hasPhone=true')
        data = response.get_json()
        print(f"   Result: {data}")

if __name__ == "__main__":
    test_export_count_directly()
