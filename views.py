from conf import app
from models import db, User, Article, Category, ArticleCategoryRelation
from decorators import templated
from flask import url_for, redirect, flash, abort
from forms import UserForm
import sqlalchemy

@app.route('/')
@templated('index.html')
def index():
    return dict(message="Hello")


@app.route('/register',methods=['GET','POST'])
@templated('forms/user_register.html')
def user_register():
    userform = UserForm()
    if userform.is_submitted():
        if userform.validate():
            user = User.initWIthForm(userform)
            db.session.add(user)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                flash('账户已使用!')
            else:
                flash('创建成功{0}'.format(user))
        else:
            flash(userform.unsuccessed)
    return dict(form=userform)


@app.route('/markdown/<md_name>',methods=['GET','POST'])
@templated('markdown.html')
def markdown(md_name):
    if not md_name in app.config['MD_FILES']:
        abort(404)

    thefile = app.config['MD_FILES'][md_name]
    md = ""
    with open(thefile,'rb') as f:
        md = f.read().decode('utf-8')
    return dict(message="nihao",md=md)

if __name__ == '__main__':
    app.run()
