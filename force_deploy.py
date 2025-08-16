#!/usr/bin/env python3
"""
Script to verify current deployment commit and trigger forced redeploy if needed
"""
import os
import requests
import subprocess
import sys

def get_current_commit():
    """Get current git commit hash"""
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def get_heroku_release():
    """Get current Heroku release info"""
    try:
        result = subprocess.run(['heroku', 'releases', '-a', 'csdl-thptdian-thongtinhocsinh', '--json'], capture_output=True, text=True)
        if result.returncode == 0:
            import json
            releases = json.loads(result.stdout)
            if releases:
                latest = releases[0]
                return latest.get('version'), latest.get('commit_id')
    except:
        pass
    return None, None

def check_api_status():
    """Check if API is working with new schema"""
    try:
        response = requests.get('https://thongtinhocsinh.site/api/students', timeout=10)
        if response.status_code == 200:
            return True, "API working"
        else:
            return False, f"API error: {response.status_code}"
    except Exception as e:
        return False, f"API error: {str(e)}"

def main():
    print("🔍 Checking deployment status...")
    
    # Get current commit
    current_commit = get_current_commit()
    print(f"📝 Current local commit: {current_commit}")
    
    # Get Heroku release
    version, heroku_commit = get_heroku_release()
    print(f"🚀 Heroku release: v{version}, commit: {heroku_commit}")
    
    # Check if commits match
    if current_commit and heroku_commit:
        if current_commit.startswith(heroku_commit) or heroku_commit.startswith(current_commit):
            print("✅ Commits match")
        else:
            print("❌ Commits don't match - deployment needed")
            return False
    
    # Check API status
    api_working, api_msg = check_api_status()
    print(f"🌐 API status: {api_msg}")
    
    return api_working

if __name__ == "__main__":
    working = main()
    sys.exit(0 if working else 1)
