from conf import app, mynavbar
from models import db, User, Article, Category
from decorators import templated, login_required, admin_required
from flask import url_for, redirect, flash, abort, session, request
from forms import UserForm, LoginForm, ArticleForm
import markdown
import sqlalchemy
import nav

@app.route('/')
@login_required
@templated('index.html')
def index():
    articles =Article.query.filter(1==1).all()
    return dict(articles = articles)


@app.route('/publish',methods=['GET','POST'])
@admin_required
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
        article.body = markdown.markdown(article.body)    # 将文章转换为HTML再存入数据库
        db.session.add(article)
        db.session.commit()

        flash('文章发表成功！')

    return dict(form=articleform,title='发布文章')


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

    return dict(form=userform, title="注册",security=True)


@app.route('/login', methods=['GET', 'POST'])
@templated('forms/commonform.html')
def user_login():
    loginform = LoginForm()
    next_url = request.args.get('next')
    if loginform.validate_on_submit():
        account = loginform.account.data
        password = loginform.password.data
        user = User.query.get(account)

        if not loginform.authcode.data == session['authcode']:
            flash('验证码错误')
            return dict(form=loginform,title="登录",security=True)

        if user and user.password == password:
            session['username'] = user.nickname
            flash('登陆成功')
            if user.account == '1':
                session['admin'] = True
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('index'))

    return dict(form=loginform,title="登录",security=True)


@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    session.clear()
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
        update = newArticle.dictfy(['title','body','category_name'])
        flash(update)
        article_query.update(update)
        db.session.commit()
        flash('success')
    else:
        article.fillIntoFormData(articleform)  # fill default value into form

    return dict(form=articleform)


@app.route('/api/article', methods=['GET', 'POST'])
@templated('base.html')
def api_article():
    if not all([key in request.form for key in ['size', 'id', 'forward']]):
        flash('你误入了一个API页面哦，故意的？')
        return dict()
    try:
        size = int(request.form['size'])
        article_id = int(request.form['id'])
        forward = int(request.form['forward'])
    except Exception as e:
        abort(501)

    articles = None

    if forward== -1:    #寻找更久远的，即id号小的
        articles = Article.query.filter(Article.id <= article_id).order_by(Article.id.desc()).limit(size)
    else:     #寻找更靠近现在的，即id号大的
        articles = Article.query.filter(Article.id >= article_id).order_by(Article.id.asc()).limit(size)

    import json
    api = [article.dictfy(['title','pub_date','body']) for article in articles.all()]

    return json.dumps(api)







@app.route('/debug', methods=['GET', 'POST'])
@templated('base.html')
def debug():
    article = Article.query.filter(1==1).first()
    flash(article.jsonify(['title','category_name','body']))
    return dict()


@app.route('/authcode',methods=['GET'])
def authcode():
    from authcode import makeAuthCode
    from random import randint
    character = str(randint(1000,9999))
    codePic = makeAuthCode(character)
    session['authcode'] = character
    return codePic, 200, {'Content-Type': 'image/JPEG'}


if __name__ == '__main__':
    app.run()