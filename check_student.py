import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Check student ID 201 data (PHAM NHAT QUANG)
cursor.execute('SELECT eye_diseases, gender FROM students WHERE id = 201')
result = cursor.fetchone()

if result:
    print("Student ID 201 (PHAM NHAT QUANG) - specific fields:")
    print(f"eye_diseases: '{result[0] if result[0] else 'NULL/EMPTY'}'")
    print(f"gender: '{result[1] if result[1] else 'NULL/EMPTY'}'")
else:
    print("Student ID 201 not found")

conn.close()
