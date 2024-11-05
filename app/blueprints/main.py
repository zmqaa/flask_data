from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import DataAnalysisForm, PlotForm
from app.models import File, User
from flask_login import current_user
from .utils import read_file
from .utils_plot import plot_data
from .utils_analysis import clean_data, get_descriptive_stats
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/data_display')
def data_display():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        uploaded_files = File.query.filter_by(user_id=user.id).all()
        print("Uploaded Files in index:", uploaded_files)  # 调试输出
    else:
        uploaded_files = File.query.all()
        flash('请登录')
    return render_template('data_analysis.html', uploaded_files=uploaded_files)


@main_bp.route('/data_analysis/<file_id>', methods=['GET', 'POST'])
def data_analysis(file_id):
    # 获取数据
    data_form = DataAnalysisForm()
    file = File.query.get_or_404(file_id)
    data = read_file(file.file_path)
    # 提取列名
    columns = data.columns.tolist()
    numeric_columns = data.select_dtypes(include='number').columns.tolist()

    # 填充data_form
    data_form.exclude_column.choices = [(col, col) for col in columns]
    data_form.unneccessary_column.choices = [(col, col) for col in columns]

    # 初始化描述性统计，以防不满足条件不存在
    descriptive_stats = None

    if data_form.validate_on_submit():
        # 数据预处理
        fillna_method = data_form.fillna_method.data
        exclude_columns =  data_form.exclude_column.data
        unneccessary_columns = data_form.unneccessary_column.data

        cleaned_data = clean_data(data,
                                  unneccessary_columns,
                                  exclude_columns,
                                  fillna_method)

        descriptive_stats = get_descriptive_stats(cleaned_data)
        descriptive_stats = descriptive_stats.to_html()

    return render_template('data_analysis_display.html',
                           data_form=data_form,
                           descriptive_stats=descriptive_stats,
                           file=file)







