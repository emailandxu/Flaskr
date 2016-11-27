from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    account = TextField("账户", validators=[DataRequired()])
    email = TextField("邮箱", validators=[DataRequired()])
    nickname = TextField("昵称", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    description = TextAreaField("介绍", validators=[DataRequired()])
