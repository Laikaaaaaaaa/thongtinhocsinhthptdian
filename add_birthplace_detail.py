#!/usr/bin/env python3
"""
Script để thêm cột birthplace_detail vào bảng students
Support cả SQLite và PostgreSQL
"""

import sqlite3
import os
import sys

# Add current directory to path to import app config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def add_birthplace_detail_column():
    """Thêm cột birthplace_detail vào bảng students"""
    print("="*60)
    print("THÊM CỘT BIRTHPLACE_DETAIL VÀO DATABASE")
    print("="*60)
    
    try:
        # Import app config
        from app import DB_CONFIG
        
        if DB_CONFIG['type'] == 'postgresql':
            try:
                import psycopg2
                conn = psycopg2.connect(
                    host=DB_CONFIG['host'],
                    database=DB_CONFIG['database'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    port=DB_CONFIG['port']
                )
                print(f"🐘 Connected to PostgreSQL: {DB_CONFIG['database']}")
            except Exception as e:
                print(f"❌ Không thể kết nối PostgreSQL: {e}")
                return False
        else:
            # SQLite
            db_path = 'students.db'
            conn = sqlite3.connect(db_path)
            print(f"📁 Connected to SQLite: {db_path}")
        
        cursor = conn.cursor()
        
        # Kiểm tra xem cột đã tồn tại chưa
        if DB_CONFIG['type'] == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='students' AND column_name='birthplace_detail'
            """)
            existing = cursor.fetchone()
            if existing:
                print("✅ Cột birthplace_detail đã tồn tại")
                conn.close()
                return True
        else:
            cursor.execute('PRAGMA table_info(students)')
            columns = [row[1] for row in cursor.fetchall()]
            if 'birthplace_detail' in columns:
                print("✅ Cột birthplace_detail đã tồn tại")
                conn.close()
                return True
        
        # Thêm cột mới
        print("🔄 Đang thêm cột birthplace_detail...")
        
        if DB_CONFIG['type'] == 'postgresql':
            cursor.execute("ALTER TABLE students ADD COLUMN birthplace_detail TEXT")
            print("✅ Đã thêm cột birthplace_detail vào PostgreSQL!")
        else:
            cursor.execute("ALTER TABLE students ADD COLUMN birthplace_detail TEXT")
            print("✅ Đã thêm cột birthplace_detail vào SQLite!")
        
        conn.commit()
        
        # Kiểm tra lại
        if DB_CONFIG['type'] == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='students' AND column_name='birthplace_detail'
            """)
            if cursor.fetchone():
                print("✅ Xác nhận: Cột birthplace_detail đã được tạo")
        else:
            cursor.execute('PRAGMA table_info(students)')
            columns = [row[1] for row in cursor.fetchall()]
            if 'birthplace_detail' in columns:
                print("✅ Xác nhận: Cột birthplace_detail đã được tạo")
        
        # Thống kê
        cursor.execute('SELECT COUNT(*) FROM students')
        total_records = cursor.fetchone()[0]
        print(f"📊 Tổng số records trong bảng: {total_records}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = add_birthplace_detail_column()
    
    if success:
        print("\n" + "="*60)
        print("✅ HOÀN THÀNH!")
        print("Bây giờ có thể:")
        print("1. Restart app.py")
        print("2. Test form submission với field birthplaceDetail")
        print("3. Xem dữ liệu trong admin panel")
        print("="*60)
    else:
        print("\n❌ Migration thất bại!")
