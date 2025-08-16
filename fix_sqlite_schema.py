#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLite Database Migration Script for Sample Data Generation
Ensures the students table has all required columns
"""

import sqlite3
from datetime import datetime

def migrate_sqlite_for_sample_data():
    """Ensure SQLite database has all required columns for sample data"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    print("🔧 Checking SQLite database for sample data compatibility...")
    
    # Get current columns
    cursor.execute('PRAGMA table_info(students)')
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"Found {len(existing_columns)} existing columns")
    
    # Required columns for sample data generation (matching current schema)
    required_columns = {
        'email': 'TEXT',
        'full_name': 'TEXT', 
        'birth_date': 'TEXT',
        'gender': 'TEXT',
        'phone': 'TEXT',
        'class': 'TEXT',
        'current_province': 'TEXT',
        'current_ward': 'TEXT',
        'current_address_detail': 'TEXT',
        'birthplace_province': 'TEXT',
        'birthplace_ward': 'TEXT',
        'birth_cert_province': 'TEXT',
        'birth_cert_ward': 'TEXT',
        'permanent_province': 'TEXT',
        'permanent_ward': 'TEXT',
        'permanent_hamlet': 'TEXT',
        'permanent_street': 'TEXT',
        'hometown_province': 'TEXT',
        'hometown_ward': 'TEXT',
        'hometown_hamlet': 'TEXT',
        'current_hamlet': 'TEXT',
        'height': 'REAL',
        'weight': 'REAL',
        'smartphone': 'TEXT',
        'computer': 'TEXT',
        'nationality': 'TEXT',
        'ethnicity': 'TEXT',
        'created_at': 'TIMESTAMP'
    }
    
    # Check which columns are missing
    missing_columns = []
    for col_name, col_type in required_columns.items():
        if col_name not in existing_columns:
            missing_columns.append((col_name, col_type))
    
    if missing_columns:
        print(f"❌ Missing {len(missing_columns)} required columns:")
        for col_name, col_type in missing_columns:
            print(f"  - {col_name} ({col_type})")
            try:
                cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
                print(f"    ✅ Added {col_name}")
            except Exception as e:
                print(f"    ❌ Failed to add {col_name}: {e}")
    else:
        print("✅ All required columns exist!")
    
    # Test a sample insert
    test_data = {
        'email': 'test_sample_insert@test.com',
        'full_name': 'Test User',
        'birth_date': '2005-01-01',
        'gender': 'Nam',
        'phone': '0123456789',
        'class': '10A1',
        'current_province': 'Thành phố Hồ Chí Minh',
        'current_ward': 'Phường 1',
        'current_address_detail': '123 Test Street',
        'birthplace_province': 'Thành phố Hồ Chí Minh',
        'birthplace_ward': 'Phường 1',
        'birth_cert_province': 'Thành phố Hồ Chí Minh',
        'birth_cert_ward': 'Phường 1',
        'permanent_province': 'Thành phố Hồ Chí Minh',
        'permanent_ward': 'Phường 1',
        'permanent_hamlet': 'Phường 1',
        'permanent_street': '123 Test Street',
        'hometown_province': 'Thành phố Hồ Chí Minh',
        'hometown_ward': 'Phường 1',
        'hometown_hamlet': 'Phường 1',
        'current_hamlet': 'Phường 1',
        'height': 170,
        'weight': 60,
        'smartphone': 'Có',
        'computer': 'Có',
        'nationality': 'Việt Nam',
        'ethnicity': 'Kinh',
        'created_at': datetime.now().isoformat()
    }
    
    try:
        columns = ', '.join(test_data.keys())
        placeholders = ', '.join(['?' for _ in test_data.keys()])
        query = f"INSERT INTO students ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, list(test_data.values()))
        
        # Get the inserted record
        cursor.execute("SELECT id, full_name FROM students WHERE email = ?", (test_data['email'],))
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Test insert successful: ID {result[0]}, Name: {result[1]}")
            # Clean up test data
            cursor.execute("DELETE FROM students WHERE email = ?", (test_data['email'],))
        
        conn.commit()
        print("✅ Database is ready for sample data generation!")
        return True
        
    except Exception as e:
        print(f"❌ Test insert failed: {e}")
        print("Database may need manual intervention")
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_sqlite_for_sample_data()
