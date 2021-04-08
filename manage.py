import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db

# app = create_app(os.getenv('production') or 'dev')
app = create_app('dev')
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

# Serve the react app as static files
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__=='__main__':
    manager.run()


#scripts
# python3 manage.py db init
# export SQLALCHEMY_DATABASE_URI=
# python3 manage.py db migrate
# python3 manage.py db upgrade
# python3 manage.py db --help