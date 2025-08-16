import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Search for student with name containing PHAM or QUANG
cursor.execute("SELECT id, full_name, class, gender FROM students WHERE full_name LIKE '%PHAM%' OR full_name LIKE '%QUANG%'")
results = cursor.fetchall()

print(f'Found {len(results)} students with PHAM or QUANG:')
for r in results:
    print(f'ID: {r[0]}, Name: {r[1]}, Class: {r[2]}, Gender: {r[3]}')

# Also check if there are any students with real data (not sample)
cursor.execute("SELECT id, full_name, class, gender FROM students WHERE email NOT LIKE '%sample%' LIMIT 10")
real_results = cursor.fetchall()

print(f'\nFound {len(real_results)} non-sample students:')
for r in real_results:
    print(f'ID: {r[0]}, Name: {r[1]}, Class: {r[2]}, Gender: {r[3]}')

conn.close()
