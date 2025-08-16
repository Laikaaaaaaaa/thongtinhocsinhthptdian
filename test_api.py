"""
Script test API để thêm học sinh mẫu qua HTTP requests
"""

import requests
import random
from datetime import datetime, timedelta

# URL của ứng dụng trên Heroku
BASE_URL = "https://thongtinhocsinh.site"
# BASE_URL = "https://csdl-thptdian-thongtinhocsinh-e0dcf61c2144.herokuapp.com"

def test_api_connection():
    """Test kết nối API"""
    try:
        response = requests.get(f"{BASE_URL}/api/students", timeout=10)
        print(f"🔗 API Connection: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Current students count: {data.get('pagination', {}).get('total_records', 0)}")
            return True
        else:
            print(f"❌ API Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def create_sample_student():
    """Tạo một học sinh mẫu qua API"""
    
    first_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ', 'Đặng']
    middle_names = ['Văn', 'Thị', 'Minh', 'Hoàng', 'Quang', 'Hữu', 'Thanh', 'Anh', 'Thành', 'Bảo']
    last_names = ['An', 'Bình', 'Cường', 'Dũng', 'Đức', 'Giang', 'Hà', 'Hải', 'Khang', 'Linh']
    
    classes = ['10A1', '10A2', '10A3', '10A4', '10A5', '10A6', '10A7', '10A8']
    genders = ['Nam', 'Nữ']
    
    # Generate random student data
    first_name = random.choice(first_names)
    middle_name = random.choice(middle_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {middle_name} {last_name}"
    
    # Create unique email
    timestamp = int(datetime.now().timestamp())
    email = f"test.student.{timestamp}@gmail.com"
    
    # Random birth date (15-18 years old)
    birth_year = random.randint(2006, 2009)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"
    
    student_data = {
        "email": email,
        "full_name": full_name,
        "nickname": last_name,
        "class": random.choice(classes),
        "birth_date": birth_date,
        "gender": random.choice(genders),
        "phone": f"0{random.randint(300000000, 999999999)}",
        "permanent_street": "123 Đường ABC",
        "permanent_hamlet": "Khu phố 1",
        "permanent_ward": "Phường Dĩ An",
        "permanent_province": "Bình Dương",
        "current_street": "123 Đường ABC",
        "current_hamlet": "Khu phố 1", 
        "current_ward": "Phường Dĩ An",
        "current_province": "Bình Dương"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/save-student",
            json=student_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Created student: {full_name} - {email}")
            return True
        else:
            print(f"❌ Failed to create student: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating student: {e}")
        return False

def main():
    """Main function to test API"""
    print("🧪 Testing THPT Dĩ An API")
    print("=" * 50)
    
    # Test connection first
    if not test_api_connection():
        print("❌ Cannot connect to API. Check if app is running.")
        return
    
    print("\n🎯 Testing student creation...")
    
    # Try to create a few students
    success_count = 0
    total_attempts = 3
    
    for i in range(total_attempts):
        print(f"\n📝 Creating student {i+1}/{total_attempts}...")
        if create_sample_student():
            success_count += 1
        
    print("\n" + "=" * 50)
    print(f"✅ Successfully created: {success_count}/{total_attempts} students")
    
    # Test connection again to see updated count
    print("\n🔄 Final check...")
    test_api_connection()

if __name__ == "__main__":
    main()
