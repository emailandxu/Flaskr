from flask import Flask
from flask_bootstrap import Bootstrap
import markdown

app = Flask(__name__)
Bootstrap(app)

app.jinja_env.trim_blocks = True

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flaskr.db"

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'hello'

app.config['SERVER_NAME'] = 'localhost:8000'

app.config['MD_FILES'] = {'开发日记': r"./开发日记.md"}


#Define jinjia filters
@app.template_filter('markdown')
def markdown_filter(md_text):
	return markdown.markdown(md_text)
