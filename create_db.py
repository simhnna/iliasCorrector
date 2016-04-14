#!flask/bin/python
from migrate.versioning import api
from corrector import db, app
import os.path

migrations = app.config['SQLALCHEMY_MIGRATE_REPO']
database = app.config['SQLALCHEMY_DATABASE_URI']

db.create_all()
if not os.path.exists(migrations):
    api.create(migrations, 'database repository')
    api.version_control(database, migrations)
else:
    api.version_control(database, migrations, api.version(migrations))
