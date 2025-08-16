import app

print('🔍 Checking database...')

# Check if we have any students
conn = app.get_db_connection()
cursor = conn.cursor()

try:
    cursor.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]
    print(f'📊 Current student count: {count}')
    
    if count == 0:
        print('🚨 No students found! Need to create data via API...')
    else:
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
    print('🔧 Trying to create students table...')
    
    if app.DB_CONFIG['type'] == 'postgresql':
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            ho_ten VARCHAR(255) NOT NULL,
            lop VARCHAR(50),
            ngay_sinh DATE,
            gioi_tinh VARCHAR(10),
            sdt VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW()
        )
        ''')
    else:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            class TEXT,
            birth_date DATE,
            gender TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    conn.commit()
    print('✅ Students table created!')
    
finally:
    conn.close()
