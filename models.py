"""Models for Blogly."""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

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
      # Relationship with User
      user = db.relationship('User', backref=db.backref('posts', lazy=True))

      # Relationship with Tag through PostTag
      tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')

class Tag(db.Model):
       __tablename__ = 'tags'

       id = db.Column(db.Integer, primary_key=True, autoincrement=True)
       name = db.Column(db.String(30), nullable=False, unique=True)

       # Relationship with Post through PostTag
       posts = db.relationship('Post', secondary='post_tags', back_populates='tags')


class PostTag(db.Model):
      """Joins together a 'Post' and a "Tag'"""

      __tablename__ = 'post_tags'
      
      # foreign keys
      post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
      tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True, nullable=False)

    






    



