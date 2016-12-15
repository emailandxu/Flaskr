from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from util import passwdMd5


class UserForm(FlaskForm):
    account = TextField("账户", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()], filters=[passwdMd5])
    nickname = TextField("昵称", validators=[DataRequired()])
    email = TextField("邮箱", validators=[DataRequired()])
    description = TextAreaField("介绍", validators=[DataRequired()])
    submit = SubmitField("注册")


class LoginForm(FlaskForm):
    account = TextField("账户", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()], filters=[passwdMd5])
    authcode = TextField("验证码", validators=[DataRequired()])
    submit = SubmitField("登录")


class ArticleForm(FlaskForm):
    title = TextField("标题", validators=[DataRequired()])
    category_name = TextField("类型", validators=[DataRequired()])
    body = TextAreaField("正文")
    submit = SubmitField("发布")
