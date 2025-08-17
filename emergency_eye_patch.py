
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
