from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import hashlib

def passwdMd5(data):
    md5_value=data
    if data:
        md5_value = hashlib.md5(data.encode('utf-8')).hexdigest()
    return md5_value

class UserForm(FlaskForm):
    account = TextField("账户", validators=[DataRequired()])
    email = TextField("邮箱", validators=[DataRequired()])
    nickname = TextField("昵称", validators=[DataRequired()])
    
    password = PasswordField("密码", validators=[DataRequired()],filters=[passwdMd5])

    description = TextAreaField("介绍", validators=[DataRequired()])

class LoginForm(FlaskForm):
    account = TextField("账户", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()],filters=[passwdMd5])
    
