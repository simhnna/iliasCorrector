import os

from flask import Flask, render_template, g
from flask.ext.sqlalchemy import SQLAlchemy

from contextlib import closing
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'migrations')

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

from corrector import views, models
