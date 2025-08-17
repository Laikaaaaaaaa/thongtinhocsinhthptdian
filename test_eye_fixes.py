#!/usr/bin/env python3

"""
Test script for the eye diseases bug fixes
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"  # Change to your production URL if needed
TEST_EMAIL = "test@example.com"

def test_save_partial_update():
    """Test that saving with missing eye_diseases field doesn't overwrite existing data"""
    print("=== Testing Save Partial Update ===")
    
    # First, save a student with eye diseases data
    full_data = {
        "email": TEST_EMAIL,
        "fullName": "Test Student",
        "class": "10A1",
        "eyeDiseases": "viễn thị,loạn thị"
    }
    
    response = requests.post(f"{BASE_URL}/api/save-student", json=full_data)
    print(f"Initial save response: {response.status_code}")
    if response.status_code == 200:
        print("✓ Initial save successful")
    else:
        print(f"✗ Initial save failed: {response.text}")
        return
    
    # Now try to update with partial data (no eye diseases field)
    partial_data = {
        "email": TEST_EMAIL,
        "fullName": "Test Student Updated",
        "class": "10A1"
        # Note: No eyeDiseases field
    }
    
    response = requests.post(f"{BASE_URL}/api/save-student", json=partial_data)
    print(f"Partial update response: {response.status_code}")
    if response.status_code == 200:
        print("✓ Partial update successful")
    else:
        print(f"✗ Partial update failed: {response.text}")
        return
    
    # Check that eye diseases data is still there
    response = requests.get(f"{BASE_URL}/api/student-by-email", params={"email": TEST_EMAIL})
    if response.status_code == 200:
        student_data = response.json().get('student', {})
        eye_diseases = student_data.get('eye_diseases', '')
        eyeDiseases = student_data.get('eyeDiseases', '')
        
        print(f"After partial update:")
        print(f"  eye_diseases: '{eye_diseases}'")
        print(f"  eyeDiseases: '{eyeDiseases}'")
        
        if eye_diseases and eyeDiseases:
            print("✓ Eye diseases data preserved after partial update")
        else:
            print("✗ Eye diseases data was lost during partial update")
    else:
        print(f"✗ Failed to retrieve updated student: {response.text}")

def test_api_response_format():
    """Test that API responses include both eye_diseases and eyeDiseases"""
    print("\n=== Testing API Response Format ===")
    
    response = requests.get(f"{BASE_URL}/api/student-by-email", params={"email": TEST_EMAIL})
    if response.status_code == 200:
        student_data = response.json().get('student', {})
        
        has_eye_diseases = 'eye_diseases' in student_data
        has_eyeDiseases = 'eyeDiseases' in student_data
        
        print(f"Response contains 'eye_diseases': {has_eye_diseases}")
        print(f"Response contains 'eyeDiseases': {has_eyeDiseases}")
        
        if has_eye_diseases and has_eyeDiseases:
            eye_diseases_val = student_data.get('eye_diseases', '')
            eyeDiseases_val = student_data.get('eyeDiseases', '')
            print(f"eye_diseases value: '{eye_diseases_val}'")
            print(f"eyeDiseases value: '{eyeDiseases_val}'")
            
            if eye_diseases_val == eyeDiseases_val:
                print("✓ Both fields have the same value")
            else:
                print("✗ Fields have different values")
        else:
            print("✗ Missing one or both field formats")
    else:
        print(f"✗ Failed to retrieve student: {response.text}")

if __name__ == "__main__":
    try:
        test_save_partial_update()
        test_api_response_format()
        print("\n=== Test Summary ===")
        print("If all tests show ✓, the bug fixes are working correctly.")
        print("If any tests show ✗, there may be additional issues to address.")
    except Exception as e:
        print(f"Test failed with error: {e}")
        print("Make sure the server is running and accessible.")
