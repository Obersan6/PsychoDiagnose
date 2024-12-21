
import unittest
from flask import session
from src.main.app import create_app, db
from src.application.models import User, Category, Disorder
from src.config import TestingConfig


class DSMBlueprintTestCase(unittest.TestCase):
    """Test cases for DSM blueprint."""

    def setUp(self):
        """Set up test app and database."""
        self.app = create_app(config_class=TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        db.create_all()

        # Add a test user
        self.test_user = User.signup(
            username="testuser",
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="password"
        )
        db.session.commit()

        self.test_user_id = self.test_user.id

    def tearDown(self):
        """Tear down the database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        """Simulate logging in the test user."""
        with self.client.session_transaction() as session:
            session['user_id'] = self.test_user_id

    def test_show_categories(self):
        """Test the categories route."""
        self.login_test_user()  # Simulate login
        with self.client as c:
            response = c.get("/categories")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Diagnostic Categories", response.data)

    def test_show_disorders(self):
        """Test the disorders route."""
        self.login_test_user()  # Simulate login
        with self.client as c:
            response = c.get("/disorders")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"List of Disorders", response.data)

    def test_get_disorder(self):
        """Test the specific disorder route."""
        with self.app.app_context():
            test_category = Category(name="Test Category", description="Test Description")
            db.session.add(test_category)
            db.session.commit()

            test_disorder = Disorder(
                name="Test Disorder",
                description="Test Description",
                criteria="Test Criteria",
                category_id=test_category.id
            )
            db.session.add(test_disorder)
            db.session.commit()

            disorder_id = test_disorder.id

        self.login_test_user()  # Simulate login
        with self.client as c:
            response = c.get(f"/disorders/{disorder_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Test Disorder", response.data)


if __name__ == "__main__":
    unittest.main()

