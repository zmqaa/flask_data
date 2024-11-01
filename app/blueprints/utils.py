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

def clean_data(data, unneccessary_columns=None):
    # 删除重复行
    data = data.drop_duplicates()

    # 填充缺失值
    data = data.fillna(method='ffill')  # 向前填充

    # 转换数据类型（示例：将日期列转换为日期格式）
    if 'date_column' in data.columns:
        data['date_column'] = pd.to_datetime(data['date_column'], errors='coerce')

    # 去除不必要的列
    if unneccessary_columns:
        data = data.drop(columns=unneccessary_columns, errors='ignore')

    return data

def get_original_metrics(data):
    metrics = {
        '大小': data.shape,    # 元组(行数，列数)
        '列名': data.columns.tolist(),    # 列名的列表
        '缺失值': data.isnull().sum().to_dict(),   # 字典 {'c1': 0, 'c2':1}...
        '列类型': data.dtypes.to_dict()   #字典 {'c1': int64, 'c2': float64}...
    }
    return metrics

def get_cleaned_metrics(data):
    metrics = {
        '大小': data.shape,
        '缺失值': data.isnull().sum().to_dict(),
        '类型': data.dtypes.to_dict()
    }
    return metrics

def get_descriptive_stats(data):
    stats = {
        "均值": data.mean(numeric_only=True),
        "标准差": data.std(numeric_only=True),
        "最小值": data.min(numeric_only=True),
        "最大值": data.max(numeric_only=True),
    }
    # 创建成dataframe,字典的key为行
    stats_df = pd.DataFrame(stats)
    # 计数
    stats_df = stats_df.style.format('{:.2f}')
    return stats_df
