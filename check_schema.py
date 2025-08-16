#!/usr/bin/env python3
import os
import psycopg2

# Connect to database
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Check if students table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'students'
        );
    """)
    table_exists = cursor.fetchone()[0]
    print(f"Table 'students' exists: {table_exists}")
    
    if table_exists:
        # Get column names
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'students' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print(f"Columns in 'students' table:")
        for col_name, col_type in columns:
            print(f"  - {col_name}: {col_type}")
    else:
        print("Table 'students' does not exist!")
    
    conn.close()
else:
    print("No DATABASE_URL found!")
