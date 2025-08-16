import app

app.init_db()
print('✅ Database initialized')

# Check if we have any students
conn = app.get_db_connection()
cursor = conn.cursor()

try:
    cursor.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]
    print(f'📊 Current student count: {count}')
    
    if count == 0:
        print('🚨 No students found! Creating sample data...')
        # Create sample data
        from app import generate_sample_students
        students = generate_sample_students(10)
        
        for student in students:
            if app.DB_CONFIG['type'] == 'postgresql':
                query = """
                INSERT INTO students (email, ho_ten, lop, ngay_sinh, gioi_tinh, sdt, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            else:
                query = """
                INSERT INTO students (email, full_name, class, birth_date, gender, phone, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
            
            cursor.execute(query, (
                student['email'],
                student['full_name'],
                student['class'],
                student['birth_date'],
                student['gender'],
                student['phone'],
                student['created_at']
            ))
        
        conn.commit()
        
        # Check count again
        cursor.execute('SELECT COUNT(*) FROM students')
        new_count = cursor.fetchone()[0]
        print(f'✅ Created {new_count} students!')
    
    # Show sample data
    if app.DB_CONFIG['type'] == 'postgresql':
        cursor.execute('SELECT ho_ten, lop, email FROM students LIMIT 3')
    else:
        cursor.execute('SELECT full_name, class, email FROM students LIMIT 3')
    
    rows = cursor.fetchall()
    print('\n📋 Sample students:')
    for row in rows:
        print(f'  - {row[0]} | {row[1]} | {row[2]}')
        
except Exception as e:
    print(f'❌ Error: {e}')
finally:
    conn.close()
