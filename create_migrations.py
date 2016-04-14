#!flask/bin/python
import imp
from migrate.versioning import api
from iliasCorrector import db, app
database = app.config['SQLALCHEMY_DATABASE_URI']
migrations = app.config['SQLALCHEMY_MIGRATE_REPO']
v = api.db_version(database, migrations)
migration = migrations+ ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(database, migrations)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(database,
        migrations, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(database, migrations)
v = api.db_version(database, migrations)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
