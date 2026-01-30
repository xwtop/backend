import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.middleware.auth import token_required
from app.common.Results import Result

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_FILE_SIZE = 5 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/image', methods=['POST'])
@token_required
def upload_image():
    if 'file' not in request.files:
        return Result.bad_request('没有上传文件')
    
    file = request.files['file']
    
    if file.filename == '':
        return Result.bad_request('没有选择文件')
    
    if not allowed_file(file.filename):
        return Result.bad_request('不支持的文件类型')
    
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return Result.bad_request('文件大小超过限制（最大5MB）')
    
    original_filename = file.filename
    ext = original_filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    
    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
    file.save(filepath)
    
    file_url = f"http://localhost:5000/uploads/{new_filename}"
    
    return Result.success({
        'url': file_url,
        'filename': new_filename,
        'size': file_size
    })
