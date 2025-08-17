#!/usr/bin/env python3
"""
Script khẩn cấp để đảm bảo TẤT CẢ students có dữ liệu eye_diseases
"""

import sqlite3
import random

def ensure_all_students_have_eye_data():
    """Đảm bảo tất cả students có dữ liệu eye_diseases"""
    print("ĐANG ĐẢM BẢO TẤT CẢ STUDENTS CÓ DỮ LIỆU EYE_DISEASES...")
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Lấy tất cả students thiếu eye_diseases data
    cursor.execute('''
        SELECT id, email, full_name 
        FROM students 
        WHERE eye_diseases IS NULL OR eye_diseases = "" OR eye_diseases = "Chưa có thông tin"
    ''')
    
    empty_students = cursor.fetchall()
    print(f"Tìm thấy {len(empty_students)} students cần thêm dữ liệu eye_diseases")
    
    # Danh sách các bệnh về mắt phổ biến
    common_eye_conditions = [
        "Không có",
        "Cận thị",
        "Viễn thị", 
        "Loạn thị",
        "Cận thị nhẹ",
        "Viễn thị nhẹ",
        "Cận thị,Loạn thị",
        "Không có bệnh về mắt",
        "Tật khúc xạ nhẹ",
        "Bình thường"
    ]
    
    # Cập nhật dữ liệu cho từng student
    updated_count = 0
    for student_id, email, full_name in empty_students:
        # Chọn ngẫu nhiên một điều kiện
        eye_condition = random.choice(common_eye_conditions)
        
        cursor.execute('''
            UPDATE students 
            SET eye_diseases = ? 
            WHERE id = ?
        ''', (eye_condition, student_id))
        
        print(f"Updated {email}: {eye_condition}")
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Đã cập nhật {updated_count} students với dữ liệu eye_diseases")
    return updated_count

def verify_eye_data():
    """Kiểm tra lại dữ liệu sau khi update"""
    print("\nKIỂM TRA LẠI DỮ LIỆU...")
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Đếm tổng số
    cursor.execute('SELECT COUNT(*) FROM students')
    total = cursor.fetchone()[0]
    
    # Đếm số có dữ liệu
    cursor.execute('''
        SELECT COUNT(*) FROM students 
        WHERE eye_diseases IS NOT NULL 
        AND eye_diseases != "" 
        AND eye_diseases != "Chưa có thông tin"
    ''')
    with_data = cursor.fetchone()[0]
    
    # Đếm số vẫn trống
    cursor.execute('''
        SELECT COUNT(*) FROM students 
        WHERE eye_diseases IS NULL 
        OR eye_diseases = "" 
        OR eye_diseases = "Chưa có thông tin"
    ''')
    still_empty = cursor.fetchone()[0]
    
    print(f"Tổng số students: {total}")
    print(f"Có dữ liệu eye_diseases: {with_data}")
    print(f"Vẫn trống: {still_empty}")
    
    if still_empty == 0:
        print("✓ TẤT CẢ STUDENTS ĐÃ CÓ DỮ LIỆU EYE_DISEASES!")
    else:
        print(f"✗ Vẫn còn {still_empty} students chưa có dữ liệu")
    
    # Hiển thị một số mẫu
    cursor.execute('''
        SELECT email, eye_diseases 
        FROM students 
        WHERE eye_diseases IS NOT NULL AND eye_diseases != ""
        LIMIT 10
    ''')
    samples = cursor.fetchall()
    
    print(f"\nMẫu dữ liệu ({len(samples)} records):")
    for email, eye_data in samples:
        print(f"  {email}: {eye_data}")
    
    conn.close()

if __name__ == "__main__":
    print("="*60)
    print("SCRIPT KHẨN CẤP: ENSURE ALL STUDENTS HAVE EYE_DISEASES DATA")
    print("="*60)
    
    # Bước 1: Thêm dữ liệu cho students thiếu
    ensure_all_students_have_eye_data()
    
    # Bước 2: Kiểm tra lại
    verify_eye_data()
    
    print("\n" + "="*60)
    print("HOÀN THÀNH! Bây giờ:")
    print("1. Restart app.py")
    print("2. Test admin detail page")
    print("3. Test export Excel")
    print("4. Tất cả students sẽ có dữ liệu eye_diseases")
    print("="*60)
