"""Blogly application."""

# from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()

    return render_template('add_post_form.html', user=user, tags=tags)

# POST /users/[user-id]/posts/new --> Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form['tag_ids'] # Get selected tag IDs

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    # Associated tags with the post
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        new_post.tags.append(tag)
    
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
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

# POST route --> /posts/[post-id]/edit --> Handle editing of a post. Redirect back to the post view.
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the show_post"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    # Clear existing tags
    post.tags.clear()

    # Get selected tag IDs from the form
    tag_ids = request.form.getlist('tag_ids')
    
    # Add the selected tags to the post
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        if tag:
            post.tags.append(tag)

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

# GET route/tags --> Lists all tags, with links to the tag detail page.
@app.route('/tags')
def list_tags():
    """Lists all tags with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# GET route /tags/[tag-id] --> Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)

# GET route /tags/new --> Shows a form to add a new tag.
@app.route('/tags/new')
def add_tag():
    """Shows a form to add a new tag."""
    return render_template('add_tag_form.html')

# POST route /tags/new --> Process add form, adds tag, and redirect to tag list.  
@app.route('/tags/new', methods=['POST'])
def submit_tag():
    """Process add form, adds tag, and redirect to tag list."""
    name = request.form['name']

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect(url_for('list_tags'))

# GET route /tags/[tag-id]/edit --> Show edit form for a tag.
@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

# POST route /tags/[tag-id]/edit --> Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name']
    db.session.commit()

    return redirect(url_for('list_tags'))

# POST route /tags/[tag-id]/delete --> Delete a tag.
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for('list_tags'))
    

### **Update Routes for Posts**

# Update the route that shows a post so that it shows all the tags for that post.

# Update the routes for adding/editing posts so that it shows a listing of the tags and lets you pick which tag(s) apply to that post. (You can use whatever form element you want here: a multi-select, a list of checkboxes, or any other way you can solve this.

# <aside>
# 💡 **Hint:** The normal way to get a value from a form, `request.form['key']`, only returns *one* value from this form. To get all of the values for that key in the form, you’ll want to investigate ***.getlist***.

# </aside>

