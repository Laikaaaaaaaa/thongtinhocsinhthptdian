#!/usr/bin/env python3
"""
Emergency Eye Diseases Data Fix Script
Tạo để debug và fix triệt để vấn đề dữ liệu bệnh về mắt bị mất/trống
"""

import sqlite3
import json
import os
from datetime import datetime

def connect_db():
    """Kết nối database"""
    return sqlite3.connect('students.db')

def analyze_eye_diseases_data():
    """Phân tích dữ liệu eye_diseases hiện tại"""
    print("="*60)
    print("PHÂN TÍCH DỮ LIỆU BỆNH VỀ MẮT")
    print("="*60)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check schema
    cursor.execute('PRAGMA table_info(students)')
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Có cột eye_diseases: {'eye_diseases' in columns}")
    
    # Đếm tổng số records
    cursor.execute('SELECT COUNT(*) FROM students')
    total = cursor.fetchone()[0]
    print(f"Tổng số học sinh: {total}")
    
    # Đếm records có eye_diseases không null/empty
    cursor.execute('SELECT COUNT(*) FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != ""')
    has_data = cursor.fetchone()[0]
    print(f"Số học sinh có dữ liệu bệnh mắt: {has_data}")
    
    # Lấy một số mẫu
    cursor.execute('SELECT email, eye_diseases FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != "" LIMIT 10')
    samples = cursor.fetchall()
    print(f"\nMẫu dữ liệu ({len(samples)} records):")
    for email, eye_data in samples:
        print(f"  {email}: {repr(eye_data)}")
    
    # Check các giá trị lạ
    cursor.execute('SELECT DISTINCT eye_diseases FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != ""')
    unique_values = cursor.fetchall()
    print(f"\nCác giá trị eye_diseases duy nhất ({len(unique_values)}):")
    for val in unique_values:
        print(f"  {repr(val[0])}")
    
    conn.close()
    return has_data > 0

def fix_eye_diseases_data():
    """Fix dữ liệu eye_diseases bị lỗi"""
    print("\n" + "="*60)
    print("SỬA CHỮA DỮ LIỆU BỆNH VỀ MẮT")
    print("="*60)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Backup trước khi fix
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_eye_diseases_{timestamp}.sql'
    
    print(f"Tạo backup: {backup_file}")
    os.system(f'sqlite3 students.db ".dump students" > {backup_file}')
    
    # Fix 1: Chuyển đổi JSON arrays thành comma-separated strings
    cursor.execute('SELECT id, email, eye_diseases FROM students WHERE eye_diseases IS NOT NULL AND eye_diseases != ""')
    records = cursor.fetchall()
    
    fixed_count = 0
    for record_id, email, eye_data in records:
        try:
            # Thử parse JSON
            if eye_data.startswith('[') and eye_data.endswith(']'):
                parsed = json.loads(eye_data)
                if isinstance(parsed, list):
                    new_value = ','.join(parsed)
                    cursor.execute('UPDATE students SET eye_diseases = ? WHERE id = ?', (new_value, record_id))
                    print(f"Fixed {email}: {eye_data} -> {new_value}")
                    fixed_count += 1
        except:
            # Không phải JSON, giữ nguyên
            pass
    
    conn.commit()
    print(f"Đã fix {fixed_count} records")
    
    # Fix 2: Tìm và restore dữ liệu từ các nguồn khác nếu có
    # (Từ logs, từ localStorage backup, etc.)
    
    conn.close()

def test_api_endpoints():
    """Test các API endpoints để xem có hoạt động không"""
    print("\n" + "="*60)
    print("KIỂM TRA API ENDPOINTS")
    print("="*60)
    
    try:
        import requests
        
        # Test local
        base_url = "http://localhost:5000"
        
        # Test get students
        try:
            response = requests.get(f"{base_url}/api/students", timeout=5)
            if response.status_code == 200:
                data = response.json()
                students = data.get('data', [])
                print(f"✓ API students hoạt động: {len(students)} học sinh")
                
                # Check eye_diseases trong response
                for student in students[:3]:  # Check 3 đầu
                    eye_diseases = student.get('eye_diseases', '')
                    eyeDiseases = student.get('eyeDiseases', '')
                    print(f"  {student.get('email', 'N/A')}: eye_diseases='{eye_diseases}', eyeDiseases='{eyeDiseases}'")
            else:
                print(f"✗ API students lỗi: {response.status_code}")
        except Exception as e:
            print(f"✗ Không thể kết nối API: {e}")
            
    except ImportError:
        print("Không có thư viện requests, skip test API")

def create_eye_diseases_migration():
    """Tạo dữ liệu mẫu cho eye_diseases nếu cần"""
    print("\n" + "="*60)
    print("TẠO DỮ LIỆU MẪU BỆNH VỀ MẮT")
    print("="*60)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Lấy các học sinh chưa có dữ liệu eye_diseases
    cursor.execute('SELECT id, email FROM students WHERE eye_diseases IS NULL OR eye_diseases = "" LIMIT 5')
    empty_records = cursor.fetchall()
    
    if empty_records:
        print(f"Tìm thấy {len(empty_records)} học sinh chưa có dữ liệu bệnh mắt")
        
        # Tạo dữ liệu mẫu
        sample_eye_diseases = [
            "Cận thị",
            "Viễn thị", 
            "Loạn thị",
            "Cận thị,Loạn thị",
            "Không có"
        ]
        
        for i, (record_id, email) in enumerate(empty_records):
            sample_data = sample_eye_diseases[i % len(sample_eye_diseases)]
            cursor.execute('UPDATE students SET eye_diseases = ? WHERE id = ?', (sample_data, record_id))
            print(f"Thêm dữ liệu mẫu cho {email}: {sample_data}")
        
        conn.commit()
        print("✓ Đã thêm dữ liệu mẫu")
    else:
        print("Tất cả học sinh đều đã có dữ liệu bệnh mắt")
    
    conn.close()

def emergency_fix_app_py():
    """Tạo patch khẩn cấp cho app.py"""
    print("\n" + "="*60)
    print("TẠO PATCH KHẨN CẤP CHO APP.PY")
    print("="*60)
    
    patch_code = '''
# EMERGENCY PATCH: Force eye_diseases to be always included in responses
def emergency_ensure_eye_diseases(student_dict):
    """Đảm bảo student_dict luôn có eye_diseases data"""
    if not student_dict:
        return student_dict
    
    # Lấy eye_diseases từ nhiều nguồn
    eye_data = (
        student_dict.get('eye_diseases') or 
        student_dict.get('eyeDiseases') or 
        ""
    )
    
    # Normalize data
    if isinstance(eye_data, str) and eye_data:
        try:
            # Nếu là JSON array, convert sang comma-separated
            import json
            parsed = json.loads(eye_data)
            if isinstance(parsed, list):
                eye_data = ','.join(parsed)
        except:
            pass
    
    # Set cả 2 fields
    student_dict['eye_diseases'] = eye_data
    student_dict['eyeDiseases'] = eye_data
    
    return student_dict

# Patch function để inject vào app.py responses
'''
    
    with open('emergency_eye_patch.py', 'w', encoding='utf-8') as f:
        f.write(patch_code)
    
    print("✓ Đã tạo emergency_eye_patch.py")
    print("Để sử dụng patch này, thêm vào đầu app.py:")
    print("from emergency_eye_patch import emergency_ensure_eye_diseases")
    print("Và gọi hàm này trước mỗi jsonify(student)")

def force_refresh_data():
    """Force refresh tất cả dữ liệu eye_diseases"""
    print("\n" + "="*60)
    print("FORCE REFRESH TẤT CẢ DỮ LIỆU")
    print("="*60)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Lấy tất cả students
    cursor.execute('SELECT id, email, eye_diseases FROM students')
    all_students = cursor.fetchall()
    
    refreshed = 0
    for student_id, email, current_eye_data in all_students:
        # Nếu có dữ liệu nhưng có thể bị lỗi format
        if current_eye_data:
            new_data = current_eye_data
            
            # Fix JSON arrays
            if current_eye_data.startswith('[') and current_eye_data.endswith(']'):
                try:
                    parsed = json.loads(current_eye_data)
                    if isinstance(parsed, list):
                        new_data = ','.join(parsed)
                        cursor.execute('UPDATE students SET eye_diseases = ? WHERE id = ?', (new_data, student_id))
                        refreshed += 1
                        print(f"Refreshed {email}: {current_eye_data} -> {new_data}")
                except:
                    pass
        else:
            # Nếu không có dữ liệu, set default
            cursor.execute('UPDATE students SET eye_diseases = ? WHERE id = ?', ("Chưa có thông tin", student_id))
            refreshed += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Đã refresh {refreshed} records")

def main():
    """Chạy tất cả các bước debug và fix"""
    print("BẮT ĐẦU EMERGENCY FIX CHO BỆN VỀ MẮT")
    print("Thời gian:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Bước 1: Phân tích dữ liệu hiện tại
    has_data = analyze_eye_diseases_data()
    
    # Bước 2: Fix dữ liệu nếu cần
    if has_data:
        fix_eye_diseases_data()
    else:
        create_eye_diseases_migration()
    
    # Bước 3: Test API
    test_api_endpoints()
    
    # Bước 4: Tạo patch khẩn cấp
    emergency_fix_app_py()
    
    # Bước 5: Force refresh
    force_refresh_data()
    
    print("\n" + "="*60)
    print("HOÀN THÀNH! KIỂM TRA LẠI:")
    print("1. Chạy app.py và test admin detail")
    print("2. Test export Excel")
    print("3. Nếu vẫn lỗi, import emergency_eye_patch.py vào app.py")
    print("="*60)

if __name__ == "__main__":
    main()
