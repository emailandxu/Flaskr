from flask import Flask
from flask_bootstrap import Bootstrap
import markdown
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup


app = Flask(__name__)
Bootstrap(app)

app.jinja_env.trim_blocks = True
app.jinja_env

nav = Nav()
nav.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flaskr.db"

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'hello'

app.config['SERVER_NAME'] = 'localhost:8000'

# Define jinjia filters
@app.template_filter('markdown')
def markdown_filter(md_text):
    return markdown.markdown(md_text)

# Define navigator
@nav.navigation()
def mynavbar():
    return Navbar(
        'Flaskr',
        View('首页', 'index'),
        View('发布','publish_article'),
        View('注册','user_register'),
        Subgroup('登入/登出',
	        View('Login','user_login'),
	        View('Logout','user_logout')
	    )
    )
