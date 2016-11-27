from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flaskr.db"

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'hello'

app.config['SERVER_NAME'] = 'localhost:8000'
