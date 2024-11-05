import os

from flask import Blueprint, request, render_template, redirect, url_for, flash
from .utils import save_file, allowed_file, read_file
from .utils_analysis import clean_data, get_cleaned_metrics, get_original_metrics, get_descriptive_stats
from flask_login import current_user, login_required
from app.models import File
from app.extensions import db
from app.forms import UploadForm

file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm() #创建表单实例
    if form.validate_on_submit():   # 验证
        file = form.file.data   # 获取文件对象

        file_path, unique_filename, original_filename = save_file(file)

        if unique_filename:
            user_id = current_user.id   #获取当前用户id
            new_file = File(
                user_id=user_id,
                file_path=file_path,
                file_name=unique_filename,
                original_file_name=original_filename
            )
            db.session.add(new_file)
            db.session.commit()
            flash('上传成功')
            return redirect(url_for('file.cleaned_display', file_id=new_file.id))
        else:
            flash('不支持的文件类型')
            return redirect(url_for('file.upload'))

    return render_template('upload.html', form=form)

@file_bp.route('/delete/<int:file_id>', methods=['GET', 'POST'])
@login_required
def delete(file_id):
    file = File.query.get_or_404(file_id)
    file_path = file.file_path
    # 删掉文件夹里的
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    flash('删除成功')
    return render_template('profile.html')

@file_bp.route('/cleaned_display/<int:file_id>')
def cleaned_display(file_id):
    file = File.query.get_or_404(file_id)
    # 读取数据
    raw_data = read_file(file.file_path)
    # 清洗
    cleaned_data = clean_data(raw_data)
    # 获得指标
    original_metrics = get_original_metrics(raw_data)
    cleaned_metrics = get_cleaned_metrics(cleaned_data)
    # 将清洗后的数据转换为HTML表格
    cleaned_data_html = cleaned_data.head(10).to_html(classes='table table-striped', index=False)
    return render_template('cleaned_display.html',
                           table=cleaned_data_html,
                           original_metrics=original_metrics,
                           cleaned_metrics=cleaned_metrics)

@file_bp.route('/analysis/<int:file_id>')
def analysis(file_id):
    file = File.query.get_or_404(file_id)
    raw_data = read_file(file.file_path)
    cleaned_data = clean_data(raw_data)
    descriptive_stats = get_descriptive_stats(cleaned_data)
    descriptive_stats = descriptive_stats.to_html(classes='table table-striped', index=False)
    return render_template('analysis.html', table=descriptive_stats)