from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('选择文件', validators=[DataRequired(), ])
    submit = SubmitField('上传')
