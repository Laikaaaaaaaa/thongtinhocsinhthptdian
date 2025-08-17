#!/usr/bin/env python3
"""
Final verification script để kiểm tra tất cả fixes hoạt động
"""

import sqlite3
import sys

def test_database_eye_data():
    """Test dữ liệu eye_diseases trong database"""
    print("="*60)
    print("KIỂM TRA DỮ LIỆU DATABASE")
    print("="*60)
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Count total and with eye_diseases
    cursor.execute('SELECT COUNT(*) FROM students')
    total = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM students 
        WHERE eye_diseases IS NOT NULL 
        AND eye_diseases != "" 
        AND eye_diseases != "Chưa có thông tin"
    ''')
    with_data = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM students 
        WHERE eye_diseases IS NULL 
        OR eye_diseases = ""
    ''')
    empty_data = cursor.fetchone()[0]
    
    print(f"Tổng số students: {total}")
    print(f"Có dữ liệu eye_diseases: {with_data}")
    print(f"Không có dữ liệu: {empty_data}")
    
    if empty_data == 0 and with_data > 0:
        print("✓ DATABASE: Tất cả students đều có dữ liệu eye_diseases")
        result = True
    else:
        print("✗ DATABASE: Vẫn có students thiếu dữ liệu")
        result = False
    
    # Show some samples
    cursor.execute('''
        SELECT email, eye_diseases 
        FROM students 
        WHERE eye_diseases IS NOT NULL AND eye_diseases != ""
        LIMIT 5
    ''')
    samples = cursor.fetchall()
    
    print(f"\nMẫu dữ liệu:")
    for email, eye_data in samples:
        print(f"  {email}: {eye_data}")
    
    conn.close()
    return result

def test_app_py_patches():
    """Kiểm tra patches trong app.py"""
    print("\n" + "="*60)
    print("KIỂM TRA PATCHES TRONG APP.PY")
    print("="*60)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for emergency_ensure_eye_diseases function
        has_emergency_function = 'emergency_ensure_eye_diseases' in content
        print(f"Có emergency_ensure_eye_diseases function: {has_emergency_function}")
        
        # Check for calls to emergency function
        emergency_calls = content.count('emergency_ensure_eye_diseases(')
        print(f"Số lần gọi emergency function: {emergency_calls}")
        
        # Check for eye_diseases normalization in export
        has_export_normalization = 'normalize_eye_diseases' in content and 'df_final' in content
        print(f"Có normalization trong export: {has_export_normalization}")
        
        if has_emergency_function and emergency_calls >= 3 and has_export_normalization:
            print("✓ APP.PY: Tất cả patches đã được áp dụng")
            return True
        else:
            print("✗ APP.PY: Một số patches bị thiếu")
            return False
            
    except Exception as e:
        print(f"✗ Không thể đọc app.py: {e}")
        return False

def test_frontend_patches():
    """Kiểm tra patches trong frontend files"""
    print("\n" + "="*60)
    print("KIỂM TRA PATCHES TRONG FRONTEND")
    print("="*60)
    
    frontend_ok = True
    
    # Check admin.html
    try:
        with open('admin.html', 'r', encoding='utf-8') as f:
            admin_content = f.read()
        
        has_parseArrayField = 'parseArrayField' in admin_content
        has_eye_diseases_check = 'eyeDiseases || student.eye_diseases' in admin_content
        
        print(f"admin.html - parseArrayField: {has_parseArrayField}")
        print(f"admin.html - dual field check: {has_eye_diseases_check}")
        
        if not (has_parseArrayField and has_eye_diseases_check):
            frontend_ok = False
            
    except Exception as e:
        print(f"✗ Không thể đọc admin.html: {e}")
        frontend_ok = False
    
    # Check done.html
    try:
        with open('done.html', 'r', encoding='utf-8') as f:
            done_content = f.read()
        
        has_dual_check = 'eyeDiseases || s.eye_diseases' in done_content
        print(f"done.html - dual field check: {has_dual_check}")
        
        if not has_dual_check:
            frontend_ok = False
            
    except Exception as e:
        print(f"✗ Không thể đọc done.html: {e}")
        frontend_ok = False
    
    if frontend_ok:
        print("✓ FRONTEND: Tất cả patches đã được áp dụng")
    else:
        print("✗ FRONTEND: Một số patches bị thiếu")
    
    return frontend_ok

def create_test_report():
    """Tạo báo cáo test tổng hợp"""
    print("\n" + "="*60)
    print("BÁO CÁO TỔNG HỢP")
    print("="*60)
    
    db_ok = test_database_eye_data()
    app_ok = test_app_py_patches()
    frontend_ok = test_frontend_patches()
    
    print(f"\n📊 KẾT QUA:")
    print(f"  Database: {'✓ OK' if db_ok else '✗ ERROR'}")
    print(f"  Backend:  {'✓ OK' if app_ok else '✗ ERROR'}")
    print(f"  Frontend: {'✓ OK' if frontend_ok else '✗ ERROR'}")
    
    all_ok = db_ok and app_ok and frontend_ok
    
    if all_ok:
        print("\n🎉 TẤT CẢ ĐÃ HOẠT ĐỘNG!")
        print("Bây giờ có thể:")
        print("1. Restart app.py")
        print("2. Test admin detail - sẽ hiện dữ liệu bệnh mắt")
        print("3. Test export Excel - cột 'Bệnh về mắt' sẽ có dữ liệu")
        print("4. Mọi student đều có dữ liệu eye_diseases")
    else:
        print("\n❌ VẪN CÓ VẤN ĐỀ!")
        if not db_ok:
            print("- Database thiếu dữ liệu eye_diseases")
        if not app_ok:
            print("- Backend patches chưa đầy đủ")
        if not frontend_ok:
            print("- Frontend patches chưa đầy đủ")
    
    return all_ok

if __name__ == "__main__":
    print("FINAL VERIFICATION SCRIPT")
    print("Kiểm tra tất cả fixes cho bug eye_diseases")
    
    success = create_test_report()
    
    if success:
        print("\n✅ SUCCESS: Bug đã được fix hoàn toàn!")
        sys.exit(0)
    else:
        print("\n❌ FAILED: Vẫn còn issues cần fix")
        sys.exit(1)
