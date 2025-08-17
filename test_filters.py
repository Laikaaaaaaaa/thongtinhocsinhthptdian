import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Test province filter with correct name
cursor.execute("SELECT COUNT(*) FROM students WHERE LOWER(permanent_province) LIKE LOWER(?)", ['%đồng nai%'])
province_count = cursor.fetchone()[0]
print(f'Province filter (đồng nai): {province_count}')

cursor.execute("SELECT COUNT(*) FROM students WHERE LOWER(permanent_province) LIKE LOWER(?)", ['%Tỉnh Đồng Nai%'])
province_count2 = cursor.fetchone()[0]
print(f'Province filter (Tỉnh Đồng Nai): {province_count2}')

# Test gender filter  
cursor.execute("SELECT COUNT(*) FROM students WHERE gender IN (?, ?)", ['Nam', 'Nữ'])
gender_count = cursor.fetchone()[0]
print(f'Gender filter: {gender_count}')

# Test phone filter
cursor.execute("SELECT COUNT(*) FROM students WHERE phone IS NOT NULL AND phone != ''")
phone_count = cursor.fetchone()[0]
print(f'Phone filter: {phone_count}')

# Test combined with correct province name
cursor.execute("SELECT COUNT(*) FROM students WHERE LOWER(permanent_province) LIKE LOWER(?) AND gender IN (?, ?) AND phone IS NOT NULL AND phone != ''", ['%Tỉnh Đồng Nai%', 'Nam', 'Nữ'])
combined_count = cursor.fetchone()[0]
print(f'All filters combined (correct province): {combined_count}')

# Test combined with original search
cursor.execute("SELECT COUNT(*) FROM students WHERE LOWER(permanent_province) LIKE LOWER(?) AND gender IN (?, ?) AND phone IS NOT NULL AND phone != ''", ['%đồng nai%', 'Nam', 'Nữ'])
combined_count_old = cursor.fetchone()[0]
print(f'All filters combined (original): {combined_count_old}')

# Test total
cursor.execute("SELECT COUNT(*) FROM students")
total = cursor.fetchone()[0]
print(f'Total students: {total}')

# Let's see actual province values
cursor.execute("SELECT DISTINCT permanent_province FROM students WHERE permanent_province IS NOT NULL LIMIT 10")
provinces = cursor.fetchall()
print(f'Sample provinces: {[p[0] for p in provinces]}')

conn.close()
