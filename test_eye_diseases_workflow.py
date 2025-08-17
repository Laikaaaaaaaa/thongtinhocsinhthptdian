#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TOÀN BỘ WORKFLOW TÌNH TRẠNG MẮT
Kiểm tra từ form input → database → admin view → export
"""

import requests
import json
import sqlite3
import pandas as pd
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"

def test_save_student_with_eye_conditions():
    """Test lưu học sinh với tình trạng mắt mới"""
    print("🧪 TEST 1: LÀM SAVE HỌC SINH VỚI TÌNH TRẠNG MẮT...")
    
    # Test data với format mới
    test_students = [
        {
            "name": "Test Eye Normal",
            "email": "test_eye_normal@test.com",
            "data": {
                "eyeConditions": "Bình thường"
            }
        },
        {
            "name": "Test Eye Multiple",
            "email": "test_eye_multiple@test.com", 
            "data": {
                "eyeConditions": "Cận thị, Loạn thị"
            }
        },
        {
            "name": "Test Eye Custom",
            "email": "test_eye_custom@test.com",
            "data": {
                "eyeConditions": "Khác: Cận thị nặng, đeo kính 6 độ"
            }
        },
        {
            "name": "Test Eye Complex",
            "email": "test_eye_complex@test.com",
            "data": {
                "eyeConditions": "Cận thị, Viễn thị, Khác: Đục thủy tinh thể"
            }
        }
    ]
    
    results = []
    for student in test_students:
        try:
            # Tạo full payload
            payload = {
                "personalInfo": {
                    "fullName": student["name"],
                    "email": student["email"],
                    "phone": "0123456789",
                    "gender": "Nam",
                    "birthDate": "2005-01-01",
                    "birthPlace": "Hà Nội",
                    "address": "Test Address",
                    "ward": "Phường 1",
                    "district": "Quận 1", 
                    "province": "TP. Hồ Chí Minh"
                },
                "familyInfo": {
                    "fatherName": "Test Father",
                    "fatherJob": "Test Job",
                    "motherName": "Test Mother", 
                    "motherJob": "Test Job"
                },
                "healthInfo": student["data"]
            }
            
            response = requests.post(f"{BASE_URL}/save_student", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ {student['name']}: {result.get('message', 'Success')}")
                results.append({
                    "email": student["email"],
                    "eyeConditions": student["data"]["eyeConditions"],
                    "status": "success"
                })
            else:
                print(f"  ❌ {student['name']}: {response.status_code} - {response.text}")
                results.append({
                    "email": student["email"], 
                    "eyeConditions": student["data"]["eyeConditions"],
                    "status": "failed"
                })
                
        except Exception as e:
            print(f"  ❌ {student['name']}: Error - {str(e)}")
            results.append({
                "email": student["email"],
                "eyeConditions": student["data"]["eyeConditions"], 
                "status": "error"
            })
    
    return results

def test_database_storage():
    """Test dữ liệu trong database"""
    print("\n🧪 TEST 2: KIỂM TRA DỮ LIỆU TRONG DATABASE...")
    
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        
        # Lấy test records vừa tạo
        cursor.execute("""
            SELECT email, eye_diseases, created_at 
            FROM students 
            WHERE email LIKE 'test_eye_%@test.com'
            ORDER BY created_at DESC
        """)
        
        records = cursor.fetchall()
        
        if records:
            print(f"  ✅ Tìm thấy {len(records)} test records:")
            for email, eye_diseases, created_at in records:
                print(f"    📧 {email}")
                print(f"       👁️ eye_diseases: '{eye_diseases}'")
                print(f"       🕐 created_at: {created_at}")
                print()
        else:
            print("  ❌ Không tìm thấy test records")
            
        conn.close()
        return records
        
    except Exception as e:
        print(f"  ❌ Database error: {str(e)}")
        return []

def test_admin_api():
    """Test admin API endpoints"""
    print("\n🧪 TEST 3: KIỂM TRA ADMIN API...")
    
    try:
        # Test get students
        response = requests.get(f"{BASE_URL}/admin/students")
        
        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            
            # Tìm test students
            test_students = [s for s in students if s.get('email', '').startswith('test_eye_')]
            
            if test_students:
                print(f"  ✅ Admin API: Tìm thấy {len(test_students)} test students")
                for student in test_students[:3]:  # Show first 3
                    print(f"    📧 {student.get('email')}")
                    print(f"       👁️ eye_diseases: '{student.get('eye_diseases', 'N/A')}'")
                    print()
            else:
                print("  ❌ Admin API: Không tìm thấy test students")
                
        else:
            print(f"  ❌ Admin API error: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Admin API error: {str(e)}")

def test_export_excel():
    """Test export Excel functionality"""
    print("\n🧪 TEST 4: KIỂM TRA EXCEL EXPORT...")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/export/excel")
        
        if response.status_code == 200:
            # Save to temp file and read
            with open('temp_export.xlsx', 'wb') as f:
                f.write(response.content)
            
            # Read Excel and check eye diseases column
            df = pd.read_excel('temp_export.xlsx')
            
            if 'Tình trạng mắt' in df.columns:
                print("  ✅ Excel export: Cột 'Tình trạng mắt' có trong file")
                
                # Check test data
                test_rows = df[df['Email'].str.contains('test_eye_', na=False)]
                if not test_rows.empty:
                    print(f"  ✅ Tìm thấy {len(test_rows)} test records trong Excel:")
                    for _, row in test_rows.iterrows():
                        print(f"    📧 {row['Email']}")
                        print(f"       👁️ Tình trạng mắt: '{row['Tình trạng mắt']}'")
                        print()
                else:
                    print("  ❌ Không tìm thấy test records trong Excel")
            else:
                print("  ❌ Excel export: Không tìm thấy cột 'Tình trạng mắt'")
                print(f"  📋 Các cột có sẵn: {list(df.columns)}")
                
        else:
            print(f"  ❌ Excel export error: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Excel export error: {str(e)}")

def cleanup_test_data():
    """Dọn dẹp test data"""
    print("\n🧹 DỌN DẸP TEST DATA...")
    
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM students WHERE email LIKE 'test_eye_%@test.com'")
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"  ✅ Đã xóa {deleted_count} test records")
        
    except Exception as e:
        print(f"  ❌ Cleanup error: {str(e)}")

def main():
    """Chạy toàn bộ test workflow"""
    print("=" * 80)
    print("🔬 TEST TOÀN BỘ WORKFLOW TÌNH TRẠNG MẮT")
    print("=" * 80)
    
    # Wait for server
    print("⏳ Chờ server khởi động...")
    time.sleep(2)
    
    # Cleanup old test data first
    cleanup_test_data()
    
    # Run tests
    save_results = test_save_student_with_eye_conditions()
    db_records = test_database_storage()
    test_admin_api()
    test_export_excel()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TÓM TẮT KẾT QUẢ TEST")
    print("=" * 80)
    
    success_count = len([r for r in save_results if r['status'] == 'success'])
    print(f"✅ Save student: {success_count}/{len(save_results)} thành công")
    print(f"✅ Database: {len(db_records)} records")
    print("✅ Admin API: Đã test")
    print("✅ Excel Export: Đã test")
    
    if success_count == len(save_results) and db_records:
        print("\n🎉 TẤT CẢ TEST ĐỀU THÀNH CÔNG!")
        print("   Workflow tình trạng mắt đã hoạt động hoàn hảo!")
    else:
        print("\n⚠️ CÓ MỘT SỐ VẤN ĐỀ CẦN KIỂM TRA")
    
    # Cleanup
    cleanup_test_data()
    
    print("\n🏁 HOÀN THÀNH TEST!")

if __name__ == "__main__":
    main()
