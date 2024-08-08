# Tests app.py with unittests

import unittest
from unittest.mock import patch
from app import app, db, User, Post

class BloggyTestCase(unittest.TestCase):
    """Test app.py with unittests."""

    def setUp(self):
        """Set up the test client and test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.client = app.test_client()
        with app.app_context():
            db.create_all()  # Create the tables

            # Create a test user and post
            self.test_user = User(first_name='John', last_name='Doe', image_url='http://example.com/johndoe.jpg')
            db.session.add(self.test_user)
            db.session.commit()

            self.test_post = Post(title='Test Post', content='This is a test post.', user_id=self.test_user.id)
            db.session.add(self.test_post)
            db.session.commit()

    def tearDown(self):
        """Drop the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_homepage(self):
        """Test homepage redirection."""
        response = self.client.get('/')

        # Check the status code is 302 (redirection)
        self.assertEqual(response.status_code, 302)

        # Check the redirection location is correct
        self.assertEqual(response.location, 'http://localhost/users')

    @patch('app.User.query')
    def test_list_users(self, mock_query):
        """Test that list_users returns a list of users."""

        mock_query.all.return_value = [
            User(id=1, first_name='John', last_name='Doe'),
            User(id=2, first_name='Jane', last_name='Doe')
        ]

        response = self.client.get('/users')

        # Check status code is 200 (ok)
        self.assertEqual(response.status_code, 200)

        # Check response contains the user names
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'Jane Doe', response.data)

    def test_add_user_form(self):
        """Test the GET request to display the add user form."""
        response = self.client.get('/users/new')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the form
        self.assertIn(b'<form', response.data)  # Ensure the form is in the HTML
        self.assertIn(b'name="first_name"', response.data)  # Check for first_name input field
        self.assertIn(b'name="last_name"', response.data)  # Check for last_name input field
        self.assertIn(b'name="image_url"', response.data)  # Check for image_url input field

    def test_add_user(self):
        """Test the POST request to add a new user."""
        # Send a POST request to add a new user
        response = self.client.post('/users/new', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'image_url': 'http://example.com/johndoe.jpg'
        })

        # Check that the status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check the redirection location
        self.assertEqual(response.location, 'http://localhost/users')

        # Verify that the user was added to the database
        with app.app_context():
            user = User.query.filter_by(first_name='John', last_name='Doe').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, 'John')
            self.assertEqual(user.last_name, 'Doe')
            self.assertEqual(user.image_url, 'http://example.com/johndoe.jpg')

    def test_submit_post(self):
        """Test the POST request to add a new post for a specific user."""
        # Send a POST request to add a new post for the test user
        response = self.client.post(f'/users/{self.test_user.id}/posts/new', data={
            'title': 'My First Post',
            'content': 'This is the content of my first post.'
        })

        # Check that the status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check the redirection location
        self.assertEqual(response.location, f'http://localhost/users/{self.test_user.id}')

        # Verify that the post was added to the database
        with app.app_context():
            post = Post.query.filter_by(title='My First Post', user_id=self.test_user.id).first()
            self.assertIsNotNone(post)
            self.assertEqual(post.title, 'My First Post')
            self.assertEqual(post.content, 'This is the content of my first post.')
            self.assertEqual(post.user_id, self.test_user.id)

    def test_show_post(self):
        """Test the GET request to display a specific post."""
        # Send a GET request to retrieve the test post
        response = self.client.get(f'/posts/{self.test_post.id}')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the post title and content
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'This is a test post.', response.data)

        # Check that the response contains buttons to edit and delete the post
        self.assertIn(b'Edit', response.data)
        self.assertIn(b'Delete', response.data)

    def test_edit_post(self):
        """Test the POST request to edit a specific post."""
        # Send a POST request to edit the test post
        response = self.client.post(f'/posts/{self.test_post.id}/edit', data={
            'title': 'Updated Title',
            'content': 'Updated content.'
        })

        # Check that the status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check the redirection location
        self.assertEqual(response.location, f'http://localhost/posts/{self.test_post.id}')

        # Verify that the post was updated in the database
        with app.app_context():
            post = Post.query.get(self.test_post.id)
            self.assertEqual(post.title, 'Updated Title')
            self.assertEqual(post.content, 'Updated content.')

    def test_delete_post(self):
        """Test the POST request to delete a specific post."""
        # Send a POST request to delete the test post
        response = self.client.post(f'/posts/{self.test_post.id}/delete')

        # Check that the status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check the redirection location
        self.assertEqual(response.location, f'http://localhost/users/{self.test_user.id}')

        # Verify that the post was deleted from the database
        with app.app_context():
            post = Post.query.get(self.test_post.id)
            self.assertIsNone(post)


