from conf import app
from models import db, User, Post, Category, PostCategoryRelation
from decorators import templated
from flask import url_for, redirect, flash
from forms import UserForm


@app.route('/')
@templated('index.html')
def index():
    return dict(message="Hello")


@app.route('/r', methods=('GET', 'POST'))
def redrct():
    return redirect(url_for('user_register'))


@app.route('/register',methods=['GET','POST'])
@templated('forms/user_register.html')
def user_register():
    userform = UserForm()
    if userform.is_submitted():
        if userform.validate():
            user = User.initWIthFlaskForm(userform)
            db.session.add(user)
            db.session.commit()
        else:
            flash(userform.unsuccessed)
    return dict(form=userform)


if __name__ == '__main__':
    app.run()
