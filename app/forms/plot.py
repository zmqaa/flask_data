from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, RadioField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget   # 复选框，不用按键就能多选
from wtforms.validators import DataRequired

# class PlotForm(FlaskForm):
#     # select下拉框
#     x_column = SelectField('X轴', choices=[], validators=[DataRequired()])
#     y_column = SelectField('Y轴', choices=[], validators=[DataRequired()])
#     num_rows = IntegerField('选择行数', default=10, validators=[DataRequired()])
#     chart_type = SelectField('图表类型', choices=[
#         ('line', '线图'),
#         ('bar', '柱状图'),
#         ('scatter', '散点图'),
#         ('pie', '饼图'),
#         ('histogram', '直方图'),
#         ('box', '箱线图'),
#         ('heatmap', '热图')
#     ])
#     submit = SubmitField('生成图表')

class PlotForm(FlaskForm):
    x_column = SelectField('X轴', choices=[], validators=[DataRequired()])
    y_column = SelectField('Y轴', choices=[], validators=[DataRequired()])

    color_column = SelectField('颜色分组', choices=[])
    size_column = SelectField('大小分组', choices=[])
    sort_column = SelectField('排序字段', choices=[], validators=[DataRequired()])
    sort_order = RadioField('排序顺序', choices=[('asc', '升序'), ('desc', '降序')], default='asc')

    num_rows = IntegerField('选择行数', default=10, validators=[DataRequired()])
    chart_type = SelectField('图表类型', choices=[
        ('line', '线图'),
        ('bar', '柱状图'),
        ('scatter', '散点图'),
        ('pie', '饼图'),
        ('histogram', '直方图'),
        ('box', '箱线图'),
        ('heatmap', '热图')
    ])
    exclude_column = SelectMultipleField('不处理异常值的列',
                                         choices=[],
                                         option_widget=CheckboxInput())

    # 选择缺失值填充方法
    fillna_method = SelectField('缺失值填充方法', choices=[
        ('ffill', '向前填充'),
        ('bfill', '向后填充'),
        ('mean', '均值填充'),
        ('median', '中位数填充')
    ])
    # 选择不必要的列
    unneccessary_column = SelectMultipleField('不需要的列',
                                              choices=[],
                                              option_widget=CheckboxInput())
    submit = SubmitField('生成图表')


