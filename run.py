#! /home/katze/back/venv/bin/python3
from app import app, db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from celery import Celery


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    # app.run()

    manager.run()

    # flask.got_request_exception.connect(_rollback_db, app)
    # flask.got_request_exception.connect(_commit_db, app)

# python3 run.py
# ./run.py runserver
# ./run.py db --help
# ./run.py db init

# ./run.py db stamp head
# ./run.py db stamp migrate
