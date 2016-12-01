from conf import app
from models import db, User, Article, Category, ArticleTagRelation
from decorators import templated,login_required
from flask import url_for, redirect, flash, abort, session,request
from forms import UserForm,LoginForm
import sqlalchemy


@app.route('/')
@login_required
@templated('index.html')
def index():
    flash("Weclome dear {0}".format(session['username']))
    return dict()

@app.route('/publish')
@login_required
@templated('forms/user_login')
def publish_article():
    pass

@app.route('/register',methods=['GET','POST'])
@templated('forms/user_register.html')
def user_register():
    userform = UserForm()
    next_url = request.args.get('next')
    
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

    return dict(form=userform,action=request.url)


@app.route('/login',methods=['GET','POST'])
@templated('forms/user_login.html')
def user_login():
    loginform = LoginForm()
    next_url = request.args.get('next')
    
    if loginform.validate_on_submit():    
        account = loginform.account.data
        password = loginform.password.data
        user = User.query.get(account)
    
        if user and user.password == password:
            flash('登陆成功')       
            session['username'] = user.nickname
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('index'))
        
    return dict(form=loginform,action=request.url)


@app.route('/logout',methods=['GET','POST'])
def user_logout():
    session.pop('username')
    return redirect(url_for('index'))
	
@app.route('/markdown/<md_name>',methods=['GET','POST'])
@login_required
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
