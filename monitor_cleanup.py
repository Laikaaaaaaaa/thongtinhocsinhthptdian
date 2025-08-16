#!/usr/bin/env python3
"""
Script để monitor hệ thống auto-cleanup
"""
import os
import time
import glob
from datetime import datetime

def monitor_export_files():
    """Monitor export files in project directory"""
    patterns = ['danh_sach_*.xlsx', 'danh_sach_*.csv', 'danh_sach_*.json']
    
    print(f"🔍 Monitoring export files at {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    found_files = []
    for pattern in patterns:
        files = glob.glob(pattern)
        found_files.extend(files)
    
    if found_files:
        print(f"📄 Found {len(found_files)} export file(s):")
        for file in found_files:
            stat = os.stat(file)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime)
            age_seconds = (datetime.now() - modified).total_seconds()
            
            print(f"  • {file}")
            print(f"    Size: {size:,} bytes")
            print(f"    Created: {modified.strftime('%H:%M:%S')}")
            print(f"    Age: {age_seconds:.0f} seconds")
            print()
    else:
        print("✅ No export files found - cleanup working!")
    
    print("=" * 50)

if __name__ == "__main__":
    while True:
        try:
            monitor_export_files()
            time.sleep(10)  # Check every 10 seconds
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
