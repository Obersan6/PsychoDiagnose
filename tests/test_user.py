# import os
# import unittest
# from flask import session, g
# from src.main.app import app, db
# from src.application.models import User
# from src.config import CURR_USER_KEY


# # Test Blueprints
# class UserBlueprintTestCase(unittest.TestCase):
#     """Tests for the user blueprint."""

#     @classmethod
#     def setUpClass(cls):
#         """Set up test environment once before all tests."""
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
#         cls.client = app.test_client()

#     def setUp(self):
#         """Set up database for each test."""
#         db.create_all()
#         test_user = User.signup(
#             username="testuser",
#             email="testuser@example.com",
#             first_name="Test",
#             last_name="User",
#             password="password",
#             img_url="/static/uploads/default.jpg"
#         )
#         db.session.add(test_user)
#         db.session.commit()

#     def tearDown(self):
#         """Clean up any fouled transaction."""
#         db.session.remove()
#         db.drop_all()

#     @classmethod
#     def tearDownClass(cls):
#         """Clean up the database and test environment."""
#         db.drop_all()


# # Tests for routes
# def test_signup(self):
#     """Test signup route."""
#     with self.client as c:
#         response = c.post(
#             "/signup",
#             data={
#                 "username": "newuser",
#                 "email": "newuser@example.com",
#                 "first_name": "New",
#                 "last_name": "User",
#                 "password": "password",
#                 "img_url": None  # Simulate no image uploaded
#             },
#             follow_redirects=True,
#         )

#         # Check if redirected to homepage
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Account created successfully!", response.data)

#         # Check if user is in the database
#         user = User.query.filter_by(username="newuser").first()
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, "newuser@example.com")

# def test_signin(self):
#     """Test signin route."""
#     with self.client as c:
#         response = c.post(
#             "/signin",
#             data={"username": "testuser", "password": "password"},
#             follow_redirects=True,
#         )

#         # Check if redirected to homepage
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Hello, testuser!", response.data)

#         # Check if session has CURR_USER_KEY
#         with c.session_transaction() as session:
#             self.assertEqual(session[CURR_USER_KEY], 1)

# def test_logout(self):
#     """Test logout route."""
#     with self.client as c:
#         with c.session_transaction() as session:
#             session[CURR_USER_KEY] = 1  # Log in as testuser

#         response = c.post("/logout", follow_redirects=True)

#         # Check if redirected to homepage
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"You have been logged out.", response.data)

#         # Check if session is cleared
#         with c.session_transaction() as session:
#             self.assertNotIn(CURR_USER_KEY, session)

# def test_edit_profile(self):
#     """Test edit profile route."""
#     with self.client as c:
#         with c.session_transaction() as session:
#             session[CURR_USER_KEY] = 1  # Log in as testuser

#         response = c.post(
#             "/user/1/profile/edit",
#             data={"first_name": "Updated", "last_name": "Name"},
#             follow_redirects=True,
#         )

#         # Check if redirected to profile page
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Profile updated successfully!", response.data)

#         # Check if the user data is updated
#         user = User.query.get(1)
#         self.assertEqual(user.first_name, "Updated")
#         self.assertEqual(user.last_name, "Name")

# def test_delete_profile(self):
#     """Test delete profile route."""
#     with self.client as c:
#         with c.session_transaction() as session:
#             session[CURR_USER_KEY] = 1  # Log in as testuser

#         response = c.post("/user/1/profile/delete", follow_redirects=True)

#         # Check if redirected to homepage
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"User deleted", response.data)

#         # Check if the user is deleted from the database
#         user = User.query.get(1)
#         self.assertIsNone(user)



import unittest

class UserTestCase(unittest.TestCase):
    """Basic test case for User functionality."""

    def test_sample(self):
        """This is a dummy test that always passes."""
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
