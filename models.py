import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

# get database details from environment variables
dev_db_url = os.environ['DATABASE_URL']
test_db_url = os.environ['TEST_DATABASE_URL']
env = os.environ['FLASK_ENV']

# Use test database or dev database according to environment
database_url = test_url if env == 'test' else dev_db_url

# instantiate SQLALchemy as db
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_url=database_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Setup Album model inherits from db.model;
class Album(db.Model):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    artist = Column(String(120), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'artist':self.artist
            }


# Setup Artist model inherits from db.model;
class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            }
