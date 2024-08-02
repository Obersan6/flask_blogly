"""Models for Blogly."""

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




# class Pet(db.Model):
#     __tablename__ = 'pets'

#     # Columns
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     #"autoincrement" is like "SERIAL" in SQL
#     name = db.Column(db.String (50), nullable=False, unique=True)  --> #A string with a max of 50 char., 
#                                                                        # cannot be null, must be unique.

#     species = db.Column(db.String (30), nullable=True) --> #It can be NULL

#     hunger = db.Column(db.Integer, nullable=False, default=20)



    



