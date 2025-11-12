
import os
import shutil
from fastapi import UploadFile # This import is for type hinting, actual UploadFile object will be passed
import uuid # For generating unique filenames

# Ensure the project directory is in sys.path for imports (e.g., config)
import sys
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import config

def save_report_file(upload_file: UploadFile, user_id: int) -> str:
    """
    Saves an uploaded report file to the configured UPLOADS_DIR.
    Returns the full path to the saved file.
    """
    # Create a user-specific subdirectory if it doesn't exist
    user_upload_dir = os.path.join(config.UPLOADS_DIR, str(user_id))
    os.makedirs(user_upload_dir, exist_ok=True)

    # Generate a unique filename to prevent clashes and store original extension
    original_filename = upload_file.filename
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    file_location = os.path.join(user_upload_dir, unique_filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return file_location
    except Exception as e:
        print(f"Error saving file: {e}")
        raise RuntimeError(f"Failed to save uploaded file: {e}")

if __name__ == '__main__':
    print("--- Testing save_report_file from within the script ---")
    # This block is for direct script execution and won't run via notebook cell
    # For notebook cell testing, the logic is replicated below.
    pass
