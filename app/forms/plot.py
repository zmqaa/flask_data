from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class PlotForm(FlaskForm):
    # select下拉框
    x_column = SelectField('X轴列', choices=[], validators=[DataRequired()])
    y_column = SelectField('Y轴列', choices=[], validators=[DataRequired()])
    num_rows = IntegerField('选择行数', default=10, validators=[DataRequired()])
    chart_type = SelectField('图表类型', choices=[('line', '线图'), ('bar', '柱状图'), ('scatter', '散点图')])
    submit = SubmitField('生成图表')