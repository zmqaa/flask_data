import pandas as pd
from flask import current_app
from werkzeug.utils import secure_filename
import os
import uuid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# 这里的file不是file模型里的file，是flask的文件对象有file.filename属性和file.save(path)方法
def save_file(file):
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = os.path.splitext(original_filename)[1]
        unique_filename = f'{uuid.uuid4()}{extension}'
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return file_path, unique_filename, original_filename
    return None, None, None

def read_file(filepath):
    extension = filepath.rsplit('.', 1)[1].lower()
    if extension == 'csv':
        df = pd.read_csv(filepath, encoding='utf-8')
    else:
        df = pd.read_excel(filepath)
    return df
