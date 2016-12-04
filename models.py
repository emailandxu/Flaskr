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

        model.set_now()                # 设置公布时间
        return model

    def fillIntoFormData(self,form):
        for field in form:
            fieldname = field.label.field_id
            try:
                getattr(form, fieldname).data = getattr(self, fieldname)
            except AttributeError as e:
                print(e)

    def jsonify(self, fields):
        jsn = dict()

        for fieldname in fields:
            jsn[fieldname] = getattr(self,fieldname)

        return jsn


    def set_now(self, datetime_value=None):
        """将有pub_date属性的实例设置成现在."""

        if not hasattr(self,"pub_date"):
            return

        if datetime_value:
            self.pub_date = datetime_value
        else:
            self.pub_date = datetime.now()



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
    category_name = db.Column(db.String(40), db.ForeignKey('category.name'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return '<Article %r>' % self.title

    def __str__(self):
        return self.__repr__()


class Category(db.Model, ModelWithWTF):
    name =db.Column(db.String(40), primary_key=True)

    def __str__(self):
        return '<Category %r>' % self.name

    def __repr__(self):
        return self.__str__()


class Tag(db.Model, ModelWithWTF):
    __tablename__ = "tag"

    name = db.Column(db.String(50),primary_key=True)

    def __repr__(self):
        return '<Tag %r>' % self.name

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

# wait to implement
class ArticleTagRelation(db.Model):
    __tablename__ = "article_tag_relation"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    tag_name = db.Column(db.String(50), db.ForeignKey('tag.name'))

    def __repr__(self):
        return '<ArticleTag {0}, `{1}`>'.format(
            Article.query.get(self.article_id).title,
            Tag.query.get(self.tag_name).name)

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    db.create_all()