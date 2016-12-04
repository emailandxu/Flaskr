from conf import app
from models import db, User, Article, Category
from decorators import templated, login_required
from flask import url_for, redirect, flash, abort, session, request
from forms import UserForm, LoginForm, ArticleForm 
import sqlalchemy


@app.route('/')
@login_required
@templated('index.html')
def index():
    flash("Weclome dear {0}".format(session['username']))
    articles =Article.query.filter(1==1).all()
    return dict(articles = articles)


@app.route('/publish',methods=['GET','POST'])
@login_required
@templated('forms/user_common.html')
def publish_article():
    articleform = ArticleForm()
    if articleform.validate_on_submit():
        if not Category.query.get(articleform.name.data):
            category = Category()
            category.name = articleform.name.data
            db.session.add(category)
            db.session.commit()
        article = Article.initWIthForm(articleform)
        db.session.add(article)
        db.session.commit()

        flash('文章发表成功！')

    return dict(form=articleform)


@app.route('/register', methods=['GET', 'POST'])
@templated('forms/user_common.html')
def user_register():
    userform = UserForm()

    if userform.is_submitted():
        if userform.validate():
            user = User.initWIthForm(userform)
            db.session.add(user)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                flash('账户已使用!')
            else:
                flash('创建成功{0}'.format(user))
        else:
            flash(userform.unsuccessed)

    return dict(form=userform, action=request.url)


@app.route('/login', methods=['GET', 'POST'])
@templated('forms/user_common.html')
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

    return dict(form=loginform)


@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    session.pop('username')
    return redirect(url_for('index'))

@app.route('/markdown/<md_name>', methods=['GET', 'POST'])
@login_required
@templated('markdown.html')
def markdown(md_name):
    article = Article.query.filter(Article.title == md_name).first()

    if not article:
        abort(404)

    md = article.body
    return dict(md=md)

if __name__ == '__main__':
    app.run()
