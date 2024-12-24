import unittest
from flask import current_app
from src.main.app import create_app, db
from src.application.models import User
from src.config import TestingConfig
from src.config import CURR_USER_KEY


class HomepageBlueprintTestCase(unittest.TestCase):
    """Tests for the homepage blueprint."""

    @classmethod
    def setUpClass(cls):
        """Set up test database and populate data for the test class."""
        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

        # Add a test user
        test_user = User.signup(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="password"
        )
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database after tests."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up a new test client before each test."""
        self.client = self.app.test_client()

    def test_homepage_logged_out(self):
        """Test homepage view for logged-out users."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)  

    def test_homepage_logged_in(self):
        """Test homepage view for logged-in users."""
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = 1  # Assuming test user ID is 1

            response = c.get("/")
            self.assertEqual(response.status_code, 200)

            # Debugging: Output the rendered HTML
            print(response.data.decode())

            # Check if the relevant parts of the page are present
            self.assertIn(b"Hello, testuser", response.data)
            self.assertIn(b"PsychoDiagnose", response.data)


    def test_homepage_template(self):
        """Ensure the correct template is rendered."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)  # Adjust to match your template content.

