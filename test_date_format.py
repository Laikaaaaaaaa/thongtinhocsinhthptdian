#!/usr/bin/env python3
"""
Test date format conversion for frontend
"""
import requests
import json

BASE_URL = "https://thongtinhocsinh.site"

def test_date_format():
    """Test with dd/mm/yyyy format like frontend sends"""
    
    # Test data with dd/mm/yyyy format (exactly like frontend)
    student_data = {
        "email": "test.dateformat@gmail.com",
        "fullName": "Nguyen Van Test",
        "class": "12A1", 
        "birthDate": "15/06/2007",  # dd/mm/yyyy format
        "gender": "Nam",
        "phone": "0123456789",
        "currentProvince": "Bình Dương"
    }
    
    print(f"🧪 Testing date format: {student_data['birthDate']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/save-student",
            json=student_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Date format conversion successful!")
                return True
            else:
                print(f"❌ API returned success=false: {result.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        
    return False

if __name__ == "__main__":
    test_date_format()
