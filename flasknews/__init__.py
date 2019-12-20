from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf.csrf import CSRFProtect
import os
from flask_ckeditor import CKEditor

csrf = CSRFProtect()

app  = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

csrf.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ckeditor = CKEditor(app)

def blog_formating(content):
    return (content[:300] + '...') if len(content) > 300 else content

app.jinja_env.globals.update(blog_formating=blog_formating)

from flasknews import routes