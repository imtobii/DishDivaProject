import django
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ensures dishdiva_backend is on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dishdiva.settings")
django.setup()

from dishdiva.classes import User, AuthSystem  # Correct import
import unittest

class TestAuthSystem(unittest.TestCase):
    def setUp(self):
        self.auth = AuthSystem()

    # Test Case 1: Valid credentials
    def test_valid_login_email(self):
        self.assertTrue(self.auth.login("meow@realwebsites.com", "m30wm30w$"))
    
    def test_valid_login_username(self):
        self.assertTrue(self.auth.login("meowmeow", "m30wm30w$"))

    # Test Case 2: Wrong password
    def test_wrong_password(self):
        self.assertFalse(self.auth.login("meow@realwebsites.com", "wrongpass"))

    # Test Case 3: Short password
    def test_invalid_password(self):
        with self.assertRaises(ValueError):
            User("testuser", "test@example.com", "short")

    # Test Case 4: Invalid email
    def test_wrong_email(self):
        self.assertFalse(self.auth.login("wrong@example.com", "m30wm30w$"))

    # Test Case 7: Invalid email format
    def test_invalid_email_format(self):
        with self.assertRaises(ValueError):
            User("baduser", "invalid-email", "Pass123")

    # Test Case 10: Unregistered username
    def test_unregistered_username(self):
        self.assertFalse(self.auth.login("unknownuser", "m30wm30w$"))

    # Test Case 19: Invalid username
    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            User("_", "user@example.com", "Pass123")

if __name__ == "__main__":
    unittest.main()