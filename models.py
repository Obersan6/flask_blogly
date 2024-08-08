"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# Models

class User(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        first_name = db.Column(db.String(50), nullable = False )
        last_name = db.Column(db.String(50), nullable = False)
        image_url = db.Column(db.String(200), nullable = True)

class Post(db.Model):
      __tablename__ = 'posts'

      id = db.Column(db.Integer, primary_key = True, autoincrement = True)
      title = db.Column(db.String(150), nullable = False)
      content = db.Column(db.String(500), nullable = False)
      created_at = db.Column(db.DateTime, default = func.now())  # Automatically set to current date and time)

      # foreign key
      user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
      # Create relationship with User
      user = db.relationship('User', backref=db.backref('posts', lazy=True))




# Next, add another model, for blog posts (call it ***Post***).

# Post should have an:

# - ***id***, like for ***User***
# - ***title***
# - ***content***
# - ***created_at*** a date+time that should automatically default to the when the post is created
# - a foreign key to the ***User*** table


    



