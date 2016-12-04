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
@templated('forms/commonform.html')
def publish_article():
    articleform = ArticleForm()
    if articleform.validate_on_submit():
        if not Category.query.get(articleform.category_name.data):
            category = Category()
            category.name = articleform.category_name.data
            db.session.add(category)
            db.session.commit()
        article = Article.initWIthForm(articleform)
        db.session.add(article)
        db.session.commit()

        flash('文章发表成功！')

    return dict(form=articleform)


@app.route('/register', methods=['GET', 'POST'])
@templated('forms/commonform.html')
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
@templated('forms/commonform.html')
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


@app.route('/article/<article_title>', methods=['GET', 'POST'])
@login_required
@templated('article.html')
def article(article_title):
    article = Article.query.filter(Article.title == article_title).first()

    if not article:
        abort(404)

    md = article.body     # the article body is markdown type

    return dict(md=md)

@app.route('/modify/article/<article_title>', methods=['GET','POST'])
@login_required
@templated('forms/commonform.html')
def modify_article(article_title):
    articleform = ArticleForm()

    article_query = Article.query.filter(Article.title==article_title)
    article = article_query.first()

    if articleform.validate_on_submit():
        newArticle = Article.initWIthForm(articleform)
        update = newArticle.jsonify(['title','body','category_name'])
        flash(update)
        article_query.update(update)
        db.session.commit()
        flash('success')
    else:
        article.fillIntoFormData(articleform)  # fill default value into form

    return dict(form = articleform)


@app.route('/debug', methods=['GET', 'POST'])
@templated('flash.html')
def debug():
    article = Article.query.filter(Article.title=='开发日记').first()
    flash(article.jsonify(['title','category_name','body']))
    return dict()

if __name__ == '__main__':
    app.run()
