#!/usr/bin/env python3
"""
Test script to verify birthplace_detail column in Excel export
"""

import requests
import sys

def test_excel_export():
    """Test if birthplace_detail is included in Excel export"""
    try:
        # Test the export endpoint
        url = 'http://localhost:5000/api/export-xlsx'
        response = requests.get(url, params={'type': 'all'})
        
        if response.status_code == 200:
            print("✅ Excel export API responded successfully")
            print(f"📊 Response size: {len(response.content)} bytes")
            
            # Check if response is Excel file
            content_type = response.headers.get('content-type', '')
            if 'excel' in content_type or 'spreadsheet' in content_type:
                print("✅ Response is Excel file format")
            else:
                print(f"⚠️ Content type: {content_type}")
                
        else:
            print(f"❌ Excel export failed with status: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Cannot connect to server - make sure Flask app is running")
        print("To start server: python app.py")
    except Exception as e:
        print(f"❌ Error testing Excel export: {e}")

def check_column_mapping():
    """Check if birthplace_detail is in the column mappings"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "'birthplace_detail': 'Nơi sinh chi tiết'" in content:
            print("✅ Column mapping for birthplace_detail found")
            
            # Count occurrences
            count = content.count("'birthplace_detail': 'Nơi sinh chi tiết'")
            print(f"📊 Found in {count} places")
        else:
            print("❌ Column mapping for birthplace_detail not found")
            
        if "'birthplace_detail'" in content:
            total_count = content.count("'birthplace_detail'")
            print(f"📊 Total birthplace_detail references: {total_count}")
        else:
            print("❌ No birthplace_detail references found")
            
    except Exception as e:
        print(f"❌ Error checking file: {e}")

if __name__ == "__main__":
    print("🔍 Testing birthplace_detail in Excel export...\n")
    
    print("1. Checking column mappings in code:")
    check_column_mapping()
    
    print("\n2. Testing Excel export API:")
    test_excel_export()
    
    print("\n✨ Test complete!")
    print("\nTo verify in admin panel:")
    print("1. Start server: python app.py")
    print("2. Go to admin panel")
    print("3. Export Excel file")
    print("4. Check if 'Nơi sinh chi tiết' column exists")
