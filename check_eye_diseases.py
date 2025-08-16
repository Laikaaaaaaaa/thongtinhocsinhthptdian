import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Kiểm tra cấu trúc bảng trước
cursor.execute('PRAGMA table_info(students)')
columns = cursor.fetchall()
print('Các cột trong bảng students:')
for col in columns:
    print(f'- {col[1]} ({col[2]})')

print("\n" + "="*50)

# Kiểm tra dữ liệu bệnh về mắt
cursor.execute('SELECT id, full_name, eye_diseases FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != "" LIMIT 10')
results = cursor.fetchall()
print('Dữ liệu bệnh về mắt trong database:')
for row in results:
    print(f'ID: {row[0]}, Tên: {row[1]}, Bệnh về mắt: "{row[2]}"')

print("\n" + "="*50)

# Kiểm tra tổng số học sinh có dữ liệu bệnh về mắt
cursor.execute('SELECT COUNT(*) FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != ""')
count = cursor.fetchone()[0]
print(f'Tổng số học sinh có thông tin bệnh về mắt: {count}')

conn.close()
