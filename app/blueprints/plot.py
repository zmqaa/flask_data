from flask import Blueprint, render_template
from app.models import *
from .utils import clean_data, read_file
from .utils_plot import *
from app.forms import PlotForm


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/plot/<int:file_id>', methods=['GET', 'POST'])
def plot(file_id):
    form = PlotForm()
    # 获取数据
    file = File.query.get_or_404(file_id)
    data = read_file(file.file_path)
    cleaned_data = clean_data(data)

    # 动态选择填充框的选项，没有这个只有画图函数的话里面的choices是空的
    # SelectField里面的choices属性对象可以是一个包含元祖的列表，这个元组由(显示值，提交值)组成
    # 显示值就是下拉菜单时显示给用户的内容，提交值就是用户提交表单时传递到后端的值。
    # 不是元祖的话就只能显示一样的
    form.x_column.choices = [col for col in cleaned_data.columns]   # index对象不行，要是list，也可 cleaned_data.columns.tolist()
    form.y_column.choices = [(col, col) for col in cleaned_data.columns]

    if form.validate_on_submit():
        num_rows = form.num_rows.data
        selected_data = cleaned_data.head(num_rows)
        x_column = form.x_column.data
        y_column = form.y_column.data
        chart_type = form.chart_type.data

        #绘图
        fig = plot_data(selected_data, x_column, y_column, chart_type)

        return render_template('plot.html', fig=fig, form=form)  # 将图形传递给模板

    return render_template('plot.html', form=form)

@plot_bp.route('/plot_selected/<int:file_id>')
def plot_selected(file_id):
    return render_template('plot_select.html', file_id=file_id)