#!/usr/bin/env python3
"""
Test grade data in database
"""

import sqlite3
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_grade_data():
    """Test if we have grade data in database"""
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        
        # Test total count
        cursor.execute('SELECT COUNT(*) FROM students')
        total = cursor.fetchone()[0]
        print(f"📊 Total students: {total}")
        
        # Test grade 11 data
        cursor.execute("SELECT COUNT(*) FROM students WHERE class LIKE '11%'")
        grade11 = cursor.fetchone()[0]
        print(f"🎓 Grade 11 students: {grade11}")
        
        # Test grade 10 data  
        cursor.execute("SELECT COUNT(*) FROM students WHERE class LIKE '10%'")
        grade10 = cursor.fetchone()[0]
        print(f"🎓 Grade 10 students: {grade10}")
        
        # Test grade 12 data
        cursor.execute("SELECT COUNT(*) FROM students WHERE class LIKE '12%'")
        grade12 = cursor.fetchone()[0]
        print(f"🎓 Grade 12 students: {grade12}")
        
        # Show sample classes
        cursor.execute("SELECT DISTINCT class FROM students ORDER BY class LIMIT 20")
        classes = [row[0] for row in cursor.fetchall()]
        print(f"📋 Sample classes: {classes}")
        
        conn.close()
        
        if grade11 == 0:
            print("⚠️ NO GRADE 11 DATA FOUND! This explains why export-count returns 0.")
        else:
            print("✅ Grade 11 data exists, issue might be elsewhere.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_grade_data()
