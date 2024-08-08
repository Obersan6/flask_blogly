# Tests app.py with unittests

from unittest import TestCase
from unittest.mock import patch
from app import app, db, User, homepage, list_users   # file name we're importing to do our testings

# Test cases

class BloggyTestCase(TestCase):
    """Test app.py with unittests."""

    def setUp(self):
        """Set up the test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()

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

        # Check reponse contains the user names
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'Jane Doe', response.data)

#kfkafnka
import unittest
from unittest.mock import patch
from app import app, db, User

class BloggyTestCase(unittest.TestCase):
    """Test app.py with unittests."""

    def setUp(self):
        """Set up the test client and create a test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.client = app.test_client()
        with app.app_context():
            db.create_all()  # Create the tables

    def tearDown(self):
        """Drop the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_add_user_form(self):
        """Test the GET request for add_user_form."""
        response = self.client.get('/users/new')
        
        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the form
        self.assertIn(b'<form', response.data)  # Adjust this according to the actual content of your form   

    def tearDown(self):
        """Drop the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_add_user_form(self):
        """Test the GET request for add_user_form."""
        response = self.client.get('/users/new')
        
        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the form
        self.assertIn(b'<form', response.data)  # Adjust this according to the actual content of your form

    @patch('app.User.query')
    def test_add_user(self, mock_query):
        """Test the POST request for add_user."""
        # Mock the query to avoid any real database interaction
        mock_query.all.return_value = []

        # Send a POST request to add a user
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
            self.assertEqual(user.image_url, 'http://example.com/johndoe.jpg')


