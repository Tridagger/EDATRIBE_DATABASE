# 表单
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Log in')


# 新增番剧表单
class PostForm(FlaskForm):
    name_cn = StringField('中文名')
    name_en = StringField('英文名')
    episodes = StringField('集数')
    filesize = StringField('大小')
    is_dual = BooleanField('双语')
    submit = SubmitField('提交')