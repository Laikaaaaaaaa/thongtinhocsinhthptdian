import requests
import json

# Test admin API
try:
    response = requests.get('http://localhost:5000/api/admin/students')
    if response.status_code == 200:
        data = response.json()
        students = data.get('students', [])
        
        print(f'Total students: {len(students)}')
        
        # Tìm học sinh có thông tin bệnh về mắt
        for student in students:
            if student.get('eye_diseases') or student.get('eyeDiseases'):
                print(f"\nStudent ID: {student.get('id')}")
                print(f"Name: {student.get('full_name')}")
                print(f"eye_diseases: {student.get('eye_diseases')}")
                print(f"eyeDiseases: {student.get('eyeDiseases')}")
                break
        else:
            print("\nKhông tìm thấy học sinh nào có thông tin bệnh về mắt trong API response")
            
            # In ra một vài học sinh đầu tiên để debug
            print("\nVài học sinh đầu tiên:")
            for i, student in enumerate(students[:2]):
                print(f"Student {i+1}:")
                print(f"  ID: {student.get('id')}")
                print(f"  Name: {student.get('full_name')}")
                print(f"  eye_diseases: {student.get('eye_diseases')}")
                print(f"  eyeDiseases: {student.get('eyeDiseases')}")
    else:
        print(f'API request failed: {response.status_code}')
        
except Exception as e:
    print(f'Error: {e}')
