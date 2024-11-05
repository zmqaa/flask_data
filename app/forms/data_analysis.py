from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, RadioField, SelectMultipleField
from wtforms.widgets import CheckboxInput, Select
from wtforms.validators import DataRequired


class DataAnalysisForm(FlaskForm):

    # 选择不处理异常值的列
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

    submit = SubmitField('提交')