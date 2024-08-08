"""Blogly application."""

# from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_details.html', user=user, posts=posts)

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

# GET all posts
@app.route('/posts')
def show_posts():
    """Show all posts"""
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

# GET /users/[user-id]/posts/new --> Show form to add a post for that user.
@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    return render_template('add_post_form.html', user=user)

# POST /users/[user-id]/posts/new --> Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('user', user_id=user.id))

# GET /posts/[post-id] --> Show a post. Show buttons to edit and delete the post.
@app.route('/posts/<int:post_id>')  
def show_post(post_id):
    """Show a post, buttons to edit and delete the post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# GET route--> /posts/[post-id]/edit --> Show form to edit a post, and to cancel (back to user page).
@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

# POST route --> /posts/[post-id]/edit --> Handle editing of a post. Redirect back to the post view.
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the show_post"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    return redirect(url_for('show_post', post_id=post.id))

# POST route /posts/[post-id]/delete --> Delete the post.
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post. Redirect to the list of posts"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id # Get the user ID before deleting the post
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user', user_id=user_id)) # Redirect to the user's detail page






