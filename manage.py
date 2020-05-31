from flask_script import Manager
from sqlalchemy import Column, String, Integer
from datetime import datetime
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db, Album, Artist

app = create_app()

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# add data to the db tables


@manager.command
def seed():
	Artist(name='The Beatles').insert()
	Artist(name='Pink Floyd').insert()

	Album(title='Abbey Road', year='1969', artist='The Beatles').insert()
	Album(
	    title='Dark Side of the Moon',
	    year='1973',
	    artist='Pink Floyd').insert()


if __name__ == '__main__':
    manager.run()
