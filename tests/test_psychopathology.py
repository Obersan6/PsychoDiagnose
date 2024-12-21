import unittest
from flask import Flask, session
from src.main.app import create_app, db
from src.application.models import Sign, Symptom, User
from src.config import TestingConfig
from src.config import CURR_USER_KEY


class PsychopathologyBlueprintTestCase(unittest.TestCase):
    """Tests for the psychopathology blueprint."""

    def setUp(self):
        """Set up test app and database before each test."""
        self.app = create_app(config_class=TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        db.create_all()

        # Add test data
        test_user = User.signup(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="password",
            img_url="/static/uploads/default.jpg"
        )
        test_sign = Sign(name="Test Sign", description="A valid test description for a sign.")
        test_symptom = Symptom(name="Test Symptom", description="A valid test description for a symptom.")
        db.session.add_all([test_user, test_sign, test_symptom])
        db.session.commit()

        self.test_sign_id = test_sign.id
        self.test_symptom_id = test_symptom.id
        self.test_user_id = test_user.id

    def tearDown(self):
        """Tear down the database and app context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        """Simulate logging in the test user."""
        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = self.test_user_id

    def test_show_signs(self):
        """Test the /signs route."""
        self.login_test_user()  # Simulate login
        with self.client as client:
            response = client.get("/signs")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Signs", response.data)

    def test_get_sign(self):
        """Test the /signs/<int:sign_id> route."""
        self.login_test_user()  # Simulate login
        with self.client as client:
            response = client.get(f"/signs/{self.test_sign_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Test Sign", response.data)

    def test_show_symptoms(self):
        """Test the /symptoms route."""
        self.login_test_user()  # Simulate login
        with self.client as client:
            response = client.get("/symptoms")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Symptoms", response.data)

    def test_get_symptom(self):
        """Test the /symptoms/<int:symptom_id> route."""
        self.login_test_user()  # Simulate login
        with self.client as client:
            response = client.get(f"/symptoms/{self.test_symptom_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Test Symptom", response.data)


if __name__ == "__main__":
    unittest.main()

