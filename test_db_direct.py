#!/usr/bin/env python3
"""
Test export-count endpoint trực tiếp
"""

import sqlite3
from app import get_db_connection

def test_database_directly():
    print("🔍 Testing database directly...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Check total count
        cursor.execute('SELECT COUNT(*) FROM students')
        total = cursor.fetchone()[0]
        print(f"📊 Total students: {total}")
        
        # 2. Check available columns
        cursor.execute('PRAGMA table_info(students)')
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Available columns: {columns}")
        
        # 3. Check province values
        cursor.execute('SELECT DISTINCT permanent_province FROM students WHERE permanent_province IS NOT NULL LIMIT 10')
        provinces = [row[0] for row in cursor.fetchall()]
        print(f"🌍 Sample provinces: {provinces}")
        
        # 4. Check gender values
        cursor.execute('SELECT DISTINCT gender FROM students WHERE gender IS NOT NULL LIMIT 5')
        genders = [row[0] for row in cursor.fetchall()]
        print(f"👥 Sample genders: {genders}")
        
        # 5. Check phone values
        cursor.execute('SELECT COUNT(*) FROM students WHERE phone IS NOT NULL AND phone != ""')
        phone_count = cursor.fetchone()[0]
        print(f"📞 Students with phone: {phone_count}")
        
        # 6. Test specific filters
        print("\n🧪 Testing specific filters:")
        
        # Test Đồng Nai filter
        cursor.execute("SELECT COUNT(*) FROM students WHERE LOWER(permanent_province) LIKE LOWER(?)", ['%Tỉnh Đồng Nai%'])
        dong_nai_count = cursor.fetchone()[0]
        print(f"📍 Tỉnh Đồng Nai: {dong_nai_count}")
        
        # Test gender filter
        cursor.execute("SELECT COUNT(*) FROM students WHERE gender IN ('Nam', 'Nữ')", )
        gender_count = cursor.fetchone()[0]
        print(f"👥 Nam + Nữ: {gender_count}")
        
        # Test combined filter
        cursor.execute("""
            SELECT COUNT(*) FROM students 
            WHERE LOWER(permanent_province) LIKE LOWER(?) 
            AND gender IN ('Nam', 'Nữ') 
            AND phone IS NOT NULL AND phone != ''
        """, ['%Tỉnh Đồng Nai%'])
        combined_count = cursor.fetchone()[0]
        print(f"🔗 Combined filter: {combined_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_database_directly()
