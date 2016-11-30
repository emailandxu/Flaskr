from conf import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)


class ModelWithWTF():

    @classmethod
    def initWIthForm(cls, form):
        model = cls()
        for field in form:
            fieldname = field.label.field_id
            try:
                setattr(model, fieldname, getattr(form, fieldname).data)
            except AttributeError as e:
                print(e)
        return model


class User(db.Model, ModelWithWTF):
    account = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(100),nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200),nullable=True)

    def __repr__(self):
        return '<User {0},{1}>'.format(self.nickname, self.account)

    def __str__(self):
        return self.__repr__()


class Article(db.Model, ModelWithWTF):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Article %r>' % self.title

    def __str__(self):
        return self.__repr__()


class Category(db.Model, ModelWithWTF):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

    def __str__(self):
        return self.__repr__()

class Comment(db.Model,ModelWithWTF):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300),nullable = False)
    pub_date = db.Column(db.DateTime,nullable = False)

    user_account = db.Column(db.String(80), db.ForeignKey('user.account'))
    user = db.relationship('User',backref=db.backref('comments',lazy='dynamic'))

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article',backref=db.backref('comments',lazy='dynamic'))

    def __str__(self):
        return '<Comment {0},{1}>'.format(self.body, self.pub_date)

    def __repr__(self):
        return self.__str__()


class ArticleCategoryRelation(db.Model):
    __tablename__ = "article_category_relation"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<ArticleCategory {0}, `{1}`>'.format(
            Article.query.get(self.article_id).title,
            Category.query.get(self.category_id).name)

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    db.create_all()