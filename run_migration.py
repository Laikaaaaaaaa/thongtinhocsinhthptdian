#!/usr/bin/env python3
"""
Script để gọi API migration trên production server
"""

import requests
import json

def call_migration_api():
    """Gọi API migration để thêm cột birthplace_detail"""
    print("="*60)
    print("CHẠY MIGRATION TRÊN PRODUCTION SERVER")
    print("="*60)
    
    # URL của production server
    base_url = "https://thongtinhocsinh.site"
    endpoint = "/api/migrate/add-birthplace-detail"
    url = f"{base_url}{endpoint}"
    
    print(f"🌐 Calling: {url}")
    
    try:
        # Gọi API migration
        response = requests.post(url, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ {result.get('message')}")
                return True
            else:
                print(f"❌ {result.get('message')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server có thể đang bận")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến server")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting migration...")
    success = call_migration_api()
    
    if success:
        print("\n" + "="*60)
        print("✅ MIGRATION THÀNH CÔNG!")
        print("Bây giờ có thể:")
        print("1. Test form submission với field birthplaceDetail")
        print("2. Xem dữ liệu trong admin panel")
        print("3. Kiểm tra export Excel")
        print("="*60)
    else:
        print("\n❌ MIGRATION THẤT BẠI!")
        print("Kiểm tra lại server hoặc thử lại sau.")
