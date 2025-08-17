import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Check if eye_diseases column exists
cursor.execute('PRAGMA table_info(students)')
columns = cursor.fetchall()
print("Database columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n" + "="*50 + "\n")

# Check eye_diseases data
cursor.execute('SELECT email, eye_diseases FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != "" LIMIT 5')
rows = cursor.fetchall()
print(f"Found {len(rows)} records with eye_diseases data:")
for row in rows:
    print(f"Email: {row[0]}")
    print(f"eye_diseases: {repr(row[1])}")
    print("-" * 30)

conn.close()
