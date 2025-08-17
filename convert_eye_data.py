#!/usr/bin/env python3
"""
Script để chuyển đổi toàn bộ dữ liệu eye_diseases sang format mới
"""

import sqlite3
import random

def convert_eye_diseases_to_new_format():
    """Chuyển đổi tất cả dữ liệu eye_diseases sang format mới"""
    print("🔄 CHUYỂN ĐỔI DỮ LIỆU SANG FORMAT MỚI...")
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Lấy tất cả students
    cursor.execute('SELECT id, email, eye_diseases FROM students')
    all_students = cursor.fetchall()
    
    # Mapping old conditions to new format
    condition_mapping = {
        'Cận thị': 'Cận thị',
        'Viễn thị': 'Viễn thị', 
        'Loạn thị': 'Loạn thị',
        'Đục thủy tinh thể': 'Khác: Đục thủy tinh thể',
        'Thoái hóa điểm': 'Khác: Thoái hóa điểm',
        'Bệnh khô mắt': 'Khác: Khô mắt',
        'Bệnh lác': 'Lác mắt',
        'Bệnh khác về mắt': 'Khác',
        'Không có': 'Bình thường',
        'Không có bệnh về mắt': 'Bình thường',
        'Bình thường': 'Bình thường',
        'Chưa có thông tin': 'Bình thường'
    }
    
    updated_count = 0
    
    for student_id, email, current_eye_data in all_students:
        new_conditions = []
        
        if current_eye_data and current_eye_data.strip():
            # Split multiple conditions
            conditions = [c.strip() for c in current_eye_data.split(',')]
            
            for condition in conditions:
                if condition in condition_mapping:
                    mapped = condition_mapping[condition]
                    if mapped not in new_conditions:  # Avoid duplicates
                        new_conditions.append(mapped)
                else:
                    # If unknown condition, add as "Khác: condition"
                    new_conditions.append(f"Khác: {condition}")
        
        # If no conditions, set as "Bình thường"
        if not new_conditions:
            new_conditions = ['Bình thường']
        
        # Join conditions with comma and space
        new_eye_data = ', '.join(new_conditions)
        
        # Update database
        cursor.execute('UPDATE students SET eye_diseases = ? WHERE id = ?', (new_eye_data, student_id))
        
        if current_eye_data != new_eye_data:
            print(f"Updated {email}: '{current_eye_data}' → '{new_eye_data}'")
            updated_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Đã cập nhật {updated_count} records với format mới")
    return updated_count

def verify_new_format():
    """Kiểm tra format mới"""
    print("\n📊 KIỂM TRA FORMAT MỚI...")
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Count different condition types
    cursor.execute('SELECT eye_diseases, COUNT(*) FROM students GROUP BY eye_diseases ORDER BY COUNT(*) DESC')
    conditions = cursor.fetchall()
    
    print(f"Các tình trạng mắt hiện tại ({len(conditions)} loại):")
    for condition, count in conditions:
        print(f"  {condition}: {count} học sinh")
    
    # Show some samples
    cursor.execute('SELECT email, eye_diseases FROM students LIMIT 10')
    samples = cursor.fetchall()
    
    print(f"\nMẫu dữ liệu (10 records đầu):")
    for email, eye_data in samples:
        print(f"  {email}: {eye_data}")
    
    conn.close()

if __name__ == "__main__":
    print("="*60)
    print("CHUYỂN ĐỔI DỮ LIỆU TÌNH TRẠNG MẮT SANG FORMAT MỚI")
    print("="*60)
    
    # Bước 1: Chuyển đổi dữ liệu
    convert_eye_diseases_to_new_format()
    
    # Bước 2: Kiểm tra kết quả
    verify_new_format()
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH CHUYỂN ĐỔI!")
    print("Format mới:")
    print("- Bình thường: Không có vấn đề về mắt")
    print("- Cận thị, Viễn thị, Loạn thị, Lác mắt, Mù màu")
    print("- Khác: [mô tả chi tiết]")
    print("- Có thể kết hợp nhiều tình trạng: 'Cận thị, Loạn thị'")
    print("="*60)
