from flask import Blueprint, render_template
from app.models import *
from .utils import read_file
from .utils_analysis import clean_data, remove_outliers
from .utils_plot import *
from app.forms import PlotForm


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/plot/<int:file_id>', methods=['GET', 'POST'])
def plot(file_id):
    form = PlotForm()
    # 获取数据
    file = File.query.get_or_404(file_id)
    data = read_file(file.file_path)
    print(type(data))
    columns = data.columns.tolist()  # 提取列名
    numeric_columns = data.select_dtypes(include='number').columns.tolist() # 也可以include=['int', 'float']
    # 动态选择填充框的选项，没有这个只有画图函数的话里面的choices是空的
    # SelectField里面的choices属性对象可以是一个包含元祖的列表，这个元组由(显示值，提交值)组成
    # 显示值就是下拉菜单时显示给用户的内容，提交值就是用户提交表单时传递到后端的值。
    # 不是元祖的话就只能显示一样的
    # form.x_column.choices = [col for col in cleaned_data.columns]   # index对象不行，要是list，也可 cleaned_data.columns.tolist()
    # form.y_column.choices = [(col, col) for col in cleaned_data.columns]


    # 填充选择框
    form.x_column.choices = [(col, col) for col in columns]
    form.y_column.choices = [(col, col) for col in columns]
    # 当用户选择“无”时，color_column 和 size_column 的值会为 ''。在代码中，这两个字段会被转换为 None，以避免数据绘制时的 KeyError
    form.color_column.choices = [('', '无')] + [(col, col) for col in columns]
    form.size_column.choices = [('', '无')] + [(col, col) for col in numeric_columns]
    form.sort_column.choices = [(col, col) for col in numeric_columns]
    print(form.sort_column.choices)
    form.exclude_column.choices = [(col, col) for col in columns]
    form.unneccessary_column.choices = [(col, col) for col in columns]
    # 初始化fig
    fig = None

    if form.validate_on_submit():
        print("表单验证通过")
        print("表单数据:", form.data)  # 输出所有表单数据

        # 获取表单输入的
        # 数据预处理
        fillna_method = form.fillna_method.data
        unneccessary_columns = form.unneccessary_column.data
        excluded_columns = form.exclude_column.data
        cleaned_data = clean_data(data, unneccessary_columns, excluded_columns, fillna_method)
        # 其他
        chart_type = form.chart_type.data
        num_rows = form.num_rows.data
        # 根据图表所需选择字段
        x_column = form.x_column.data
        y_column = form.y_column.data
        # 在视图函数中，我们用 .data or None 的方式确保如果用户选择了“无”，下拉框字段的值会为 None，而不是空字符串。这样做可以避免 plot_data() 函数试图查找不存在的列时抛出 KeyError 错误。
        color_column = form.color_column.data or None
        size_column = form.size_column.data or None
        sort_column = form.sort_column.data
        sort_order = form.sort_order.data

        # # 清理异常值
        # excluded_columns = form.exclude_column.data
        # included_columns = []
        # for col in numeric_columns:
        #     if col not in excluded_columns:
        #         included_columns.append(col)
        # if included_columns:
        #     cleaned_data = clean_data(cleaned_data, included_columns)

        # 排序,这里排完顺序再绘图，不用传参数给绘图函数
        selected_data = cleaned_data.head(num_rows)
        ascending = (sort_order == 'asc')
        selected_data = selected_data.sort_values(by=sort_column, ascending=ascending)  #是asc的话就返回true
        # 绘图
        fig = plot_data(
            selected_data,
            x_column,
            y_column,
            chart_type,
            color_column,
            size_column
        )
        return render_template('plot.html', fig=fig, form=form)  # 将图形传递给模板
    else:
        print(form.errors)
    return render_template('plot.html', form=form)
