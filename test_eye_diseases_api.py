#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to check eye_diseases data through API
"""

import sqlite3
import json

def test_student_detail_processing():
    """Test how student detail data is processed"""
    
    # Get student data from database
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != "" LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("No student with eye_diseases found")
        return
    
    # Convert to dict like API does
    student = dict(row)
    print(f"Student ID: {student['id']}")
    print(f"Student Name: {student.get('full_name', 'N/A')}")
    print(f"Raw eye_diseases value: '{student.get('eye_diseases', '')}'")
    print(f"Type: {type(student.get('eye_diseases', ''))}")
    
    # Test API mapping like in app.py
    student['eyeDiseases'] = student.get('eye_diseases', '')
    print(f"After mapping - eyeDiseases: '{student['eyeDiseases']}'")
    
    # Test frontend parsing like in admin.html
    def parseArrayField(fieldValue):
        print(f'parseArrayField called with: {fieldValue}, type: {type(fieldValue)}')
        if not fieldValue or fieldValue == 'null' or fieldValue == 'undefined' or fieldValue == '':
            return 'Chưa có thông tin'
        
        if isinstance(fieldValue, str):
            try:
                # Try to parse as JSON first
                parsed = json.loads(fieldValue)
                if isinstance(parsed, list):
                    return ', '.join(parsed)
                return str(parsed)
            except:
                # If not JSON, try comma-separated values
                trimmed = fieldValue.strip()
                if ',' in trimmed:
                    result = ', '.join([x.strip() for x in trimmed.split(',') if x.strip()])
                    print(f'parseArrayField result: {result}')
                    return result or 'Chưa có thông tin'
                # Single value
                print(f'parseArrayField result: {trimmed}')
                return trimmed or 'Chưa có thông tin'
        
        if isinstance(fieldValue, list):
            return ', '.join(fieldValue) or 'Chưa có thông tin'
        
        return str(fieldValue) or 'Chưa có thông tin'
    
    # Test both ways frontend might access the data
    eyeData = student.get('eyeDiseases') or student.get('eye_diseases')
    print(f"Selected eyeData: '{eyeData}'")
    
    result = parseArrayField(eyeData)
    print(f"Final parsed result: '{result}'")

if __name__ == '__main__':
    test_student_detail_processing()
