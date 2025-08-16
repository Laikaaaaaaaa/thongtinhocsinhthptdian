import os
import psycopg2

# Connect to database
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()

try:
    # Update student ID 8 with some sample data for testing
    cursor.execute("""
        UPDATE students SET 
            gioi_tinh = 'Nam',
            nationality = 'Việt Nam',
            height = 175,
            weight = 65,
            eye_diseases = 'Không có',
            swimming_skill = 'Biết bơi',
            smartphone = 'Có',
            computer = 'Có',
            father_ethnicity = 'Kinh',
            mother_ethnicity = 'Kinh',
            father_birth_year = 1980,
            mother_birth_year = 1985,
            father_phone = '0987654321',
            mother_phone = '0912345678',
            permanent_province = 'Thành phố Hồ Chí Minh',
            permanent_ward = 'Phường Dĩ An',
            permanent_hamlet = 'Khu phố 1',
            permanent_street = 'Đường Nguyễn An Ninh',
            current_province = 'Thành phố Hồ Chí Minh',
            current_ward = 'Phường Dĩ An',
            current_hamlet = 'Khu phố 1'
        WHERE id = 8
    """)
    
    conn.commit()
    print("✅ Updated student ID 8 with sample data!")
    
except Exception as e:
    print(f"❌ Error updating data: {e}")
    conn.rollback()
finally:
    conn.close()
