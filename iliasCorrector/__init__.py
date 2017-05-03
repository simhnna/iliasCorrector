import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

DEBUG = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
USERNAME = 'admin'
PASSWORD = 'password'


def err404(error):
    return render_template('error.html', error=error), 404


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('CORRECTOR_SETTINGS', silent=True)
app.error_handler_spec[None][404] = err404
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from iliasCorrector import views, models
