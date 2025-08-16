#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test function directly without running web server
from app import get_db_connection, get_placeholder
import random
from datetime import datetime, timedelta

def test_generate_sample_data_direct():
    """Test function tạo data trực tiếp"""
    try:
        print("🧪 Testing generate sample data function directly...")
        
        count = 3
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Dữ liệu mẫu
        first_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng']
        middle_names = ['Văn', 'Thị', 'Minh', 'Hoàng', 'Quang']  
        last_names = ['An', 'Bình', 'Cường', 'Dũng', 'Đức']
        classes = ['10A1', '10A2', '11A1', '11A2', '12A1', '12A2']
        genders = ['Nam', 'Nữ']
        provinces = ['Thành phố Hồ Chí Minh', 'Tỉnh Đồng Nai', 'Tỉnh Bình Dương']
        
        created_count = 0
        for i in range(count):
            # Tạo tên thực tế
            first_name = random.choice(first_names)
            middle_name = random.choice(middle_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {middle_name} {last_name}"
            
            # Email học sinh mẫu
            email_name = f"sample_{last_name.lower()}.{middle_name.lower()}.{i+200:03d}_sample"
            email = f"{email_name}@test.sample.com"
            
            # Ngày sinh
            birth_year = random.randint(2005, 2008)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
            
            gender = random.choice(genders)
            phone = f"0{random.randint(700000000, 999999999)}"
            class_name = random.choice(classes)
            province = random.choice(provinces)
            ward = f"Phường {random.randint(1, 20)}"
            street_num = random.randint(1, 500)
            current_address = f"{street_num} Đường {random.randint(1, 50)}, {ward}, {province}"
            
            # Thời gian tạo
            days_ago = random.randint(0, 30)
            created_at = (datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))).isoformat()
            
            student_data = {
                'email': email,
                'full_name': full_name,
                'birth_date': birth_date,
                'gender': gender,
                'phone': phone,
                'class': class_name,
                'current_province': province,
                'current_ward': ward,
                'current_address_detail': current_address,
                'birthplace_province': province,
                'birthplace_ward': ward,
                'birth_cert_province': province,
                'birth_cert_ward': ward,
                'permanent_province': province,
                'permanent_ward': ward,
                'permanent_hamlet': ward,
                'permanent_street': f"{street_num} Đường {random.randint(1, 50)}",
                'hometown_province': province,
                'hometown_ward': ward,
                'hometown_hamlet': ward,
                'current_hamlet': ward,
                'height': random.randint(150, 180),
                'weight': random.randint(45, 75),
                'smartphone': random.choice(['Có', 'Không']),
                'computer': random.choice(['Có', 'Không']),
                'nationality': 'Việt Nam',
                'ethnicity': 'Kinh',
                'created_at': created_at
            }
            
            print(f"Creating student {i+1}: {full_name}")
            
            # Insert vào database
            columns = ', '.join(student_data.keys())
            placeholder = get_placeholder()
            placeholders = ', '.join([placeholder for _ in student_data.keys()])
            query = f"INSERT INTO students ({columns}) VALUES ({placeholders})"
            
            print(f"Query: {query[:100]}...")
            print(f"Values: {list(student_data.values())[:5]}...")
            
            cursor.execute(query, list(student_data.values()))
            created_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully created {created_count} sample students!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_generate_sample_data_direct()
