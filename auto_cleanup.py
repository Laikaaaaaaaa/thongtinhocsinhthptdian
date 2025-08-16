"""
Auto-cleanup script cho export files
Chạy định kỳ để xóa files export cũ
"""
import os
import time
import glob
from datetime import datetime, timedelta
import threading

class FileCleanupManager:
    def __init__(self, cleanup_after_minutes=5):
        self.cleanup_after_minutes = cleanup_after_minutes
        self.running = False
        self.thread = None
    
    def start(self):
        """Start cleanup manager"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._cleanup_loop)
            self.thread.daemon = True
            self.thread.start()
            print(f"🧹 Cleanup manager started - will clean files after {self.cleanup_after_minutes} minutes")
    
    def stop(self):
        """Stop cleanup manager"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("🛑 Cleanup manager stopped")
    
    def _cleanup_loop(self):
        """Main cleanup loop"""
        while self.running:
            try:
                self._cleanup_old_files()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"❌ Cleanup error: {e}")
                time.sleep(60)
    
    def _cleanup_old_files(self):
        """Clean up old export files"""
        patterns = ['danh_sach_*.xlsx', 'danh_sach_*.csv', 'danh_sach_*.json']
        cutoff_time = datetime.now() - timedelta(minutes=self.cleanup_after_minutes)
        
        for pattern in patterns:
            files = glob.glob(pattern)
            for file in files:
                try:
                    stat = os.stat(file)
                    file_time = datetime.fromtimestamp(stat.st_mtime)
                    
                    if file_time < cutoff_time:
                        os.remove(file)
                        age_minutes = (datetime.now() - file_time).total_seconds() / 60
                        print(f"🗑️ [AUTO-CLEANUP] Deleted old file: {file} (age: {age_minutes:.1f} min)")
                except Exception as e:
                    print(f"❌ [AUTO-CLEANUP] Failed to delete {file}: {e}")

# Global cleanup manager instance
cleanup_manager = FileCleanupManager(cleanup_after_minutes=2)  # 2 minutes for testing

def start_auto_cleanup():
    """Start auto cleanup"""
    cleanup_manager.start()

def stop_auto_cleanup():
    """Stop auto cleanup"""
    cleanup_manager.stop()

if __name__ == "__main__":
    print("🧹 Starting auto-cleanup for export files...")
    start_auto_cleanup()
    
    try:
        while True:
            time.sleep(10)
            
            # Show status
            patterns = ['danh_sach_*.xlsx', 'danh_sach_*.csv', 'danh_sach_*.json']
            found_files = []
            for pattern in patterns:
                found_files.extend(glob.glob(pattern))
            
            if found_files:
                print(f"📄 {len(found_files)} export files found:")
                for file in found_files:
                    stat = os.stat(file)
                    age = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 60
                    print(f"  • {file} (age: {age:.1f} min)")
            else:
                print("✅ No export files - directory clean")
            print("-" * 40)
            
    except KeyboardInterrupt:
        print("\n👋 Stopping auto-cleanup...")
        stop_auto_cleanup()
