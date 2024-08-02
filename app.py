"""Blogly application."""

# from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = "chocolate"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Caccolino5@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def homepage():
    """Redirect to list of users."""
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    """Show all users and link to the add-user form."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET'])
def add_user_form():
    """Show form to add a new user."""
    return render_template('add_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Process add-form, add new user, and go back to '/users'"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>')
def user(user_id):
    """Show info of a user, show button to their edit page and delete user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Show form to edit a user and process the form to update the user"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('user', user_id=user.id))
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the user and redirect to the list of users"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))




# MAKE ROUTES FOR:**

# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.

# **POST */users/[user-id]/delete :*** Delete the user.



