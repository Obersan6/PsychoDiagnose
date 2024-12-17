# Shared utilities file "allowed_file can be used across blueprints."

import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(upload_folder, file):
    """Save the uploaded file to the upload folder and return the relative path."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return f"/static/uploads/{filename}"  # Relative path for rendering
