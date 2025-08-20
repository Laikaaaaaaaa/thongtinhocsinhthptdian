#!/usr/bin/env python3
"""
Script to add birthplace_detail to all column mappings in app.py
"""

import re

def update_column_mappings():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find column mappings that have birthplace_province and birthplace_ward
    # but missing birthplace_detail
    pattern = r"('birthplace_province': '[^']+',\s*'birthplace_ward': '[^']+',)(\s*'current_address_detail')"
    
    replacement = r"\1\n            'birthplace_detail': 'Nơi sinh chi tiết',\2"
    
    # Replace all occurrences
    updated_content = re.sub(pattern, replacement, content)
    
    # Check if any changes were made
    if content != updated_content:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Updated column mappings to include birthplace_detail")
        
        # Count how many replacements were made
        matches = re.findall(pattern, content)
        print(f"📊 Made {len(matches)} replacements")
    else:
        print("ℹ️ No changes needed - birthplace_detail already exists in all mappings")

if __name__ == "__main__":
    update_column_mappings()
