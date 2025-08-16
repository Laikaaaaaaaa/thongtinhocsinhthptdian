import os
import psycopg2

# Connect to database
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()

# New columns to add
new_columns = [
    ('nickname', 'VARCHAR(255)'),
    ('khoi', 'VARCHAR(20)'),
    ('nationality', 'VARCHAR(100)'),
    ('citizen_id', 'VARCHAR(50)'),
    ('cccd_date', 'DATE'),
    ('cccd_place', 'VARCHAR(255)'),
    ('personal_id', 'VARCHAR(50)'),
    ('passport', 'VARCHAR(50)'),
    ('passport_date', 'DATE'),
    ('passport_place', 'VARCHAR(255)'),
    ('occupation', 'VARCHAR(255)'),
    ('organization', 'VARCHAR(255)'),
    ('permanent_province', 'VARCHAR(255)'),
    ('permanent_ward', 'VARCHAR(255)'),
    ('permanent_hamlet', 'VARCHAR(255)'),
    ('permanent_street', 'VARCHAR(255)'),
    ('hometown_province', 'VARCHAR(255)'),
    ('hometown_ward', 'VARCHAR(255)'),
    ('hometown_hamlet', 'VARCHAR(255)'),
    ('current_ward', 'VARCHAR(255)'),
    ('current_hamlet', 'VARCHAR(255)'),
    ('birthplace_province', 'VARCHAR(255)'),
    ('birthplace_ward', 'VARCHAR(255)'),
    ('birth_cert_province', 'VARCHAR(255)'),
    ('birth_cert_ward', 'VARCHAR(255)'),
    ('height', 'INTEGER'),
    ('weight', 'INTEGER'),
    ('eye_diseases', 'TEXT'),
    ('swimming_skill', 'VARCHAR(100)'),
    ('smartphone', 'VARCHAR(20)'),
    ('computer', 'VARCHAR(20)'),
    ('father_ethnicity', 'VARCHAR(100)'),
    ('father_birth_year', 'INTEGER'),
    ('father_phone', 'VARCHAR(20)'),
    ('father_cccd', 'VARCHAR(50)'),
    ('mother_ethnicity', 'VARCHAR(100)'),
    ('mother_birth_year', 'INTEGER'),
    ('mother_phone', 'VARCHAR(20)'),
    ('mother_cccd', 'VARCHAR(50)'),
    ('guardian_name', 'VARCHAR(255)'),
    ('guardian_job', 'VARCHAR(255)'),
    ('guardian_birth_year', 'INTEGER'),
    ('guardian_phone', 'VARCHAR(20)'),
    ('guardian_cccd', 'VARCHAR(50)'),
    ('guardian_gender', 'VARCHAR(10)')
]

try:
    print("Adding new columns to students table...")
    
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
            conn.commit()  # Commit each column addition separately
            print(f"✅ Added column: {col_name}")
        except psycopg2.Error as e:
            conn.rollback()  # Rollback failed transaction
            if "already exists" in str(e):
                print(f"⚠️ Column {col_name} already exists, skipping")
            else:
                print(f"❌ Error adding column {col_name}: {e}")
    
    print("✅ Database migration completed successfully!")
    
except Exception as e:
    print(f"❌ Migration failed: {e}")
    conn.rollback()
finally:
    conn.close()
