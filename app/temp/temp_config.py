# Application temporary files
import tempfile
import os

TEMP_DIR = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_DIR, 'uploads')
TEMP_FILE_EXPIRY = 3600  # seconds

# File size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg']
