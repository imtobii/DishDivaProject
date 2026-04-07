import django
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ensures dishdiva_backend is on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dishdiva.settings")
django.setup()

# test_ingredients.py

import unittest
from dishdiva.classes import User, Ingredient, Nutrition

class TestIngredientUpload(unittest.TestCase):

    def setUp(self):
        # Initialize a user and a valid nutrition object for reuse
        self.user = User("tester01", "tester@example.com", "Validpass123")
        self.valid_nutrition = Nutrition(100, 2, 5, 6)

    def try_add_ingredient(self, name, quantity):
        # Helper method to add ingredient and catch potential errors
        try:
            ingredient = Ingredient(name, "grams", self.valid_nutrition)
            self.user.add_ingredient(ingredient, quantity)
            return "Ingredients uploaded successfully"
        except ValueError as e:
            return f"Ingredient(s) could not be uploaded: {str(e)}"

    # Test Case 1: Valid ingredient name and positive quantity
    def test_valid_cheese_quantity(self):
        result = self.try_add_ingredient("Cheese", 3)
        self.assertEqual(result, "Ingredients uploaded successfully")

    # Test Case 2: Valid ingredient name but zero quantity
    def test_zero_quantity(self):
        result = self.try_add_ingredient("Cheese", 0)
        self.assertEqual(result, "Ingredient(s) could not be uploaded: Quantity must be a positive number")

    # Test Case 3: Valid ingredient name but negative quantity
    def test_negative_quantity(self):
        result = self.try_add_ingredient("Cheese", -3)
        self.assertEqual(result, "Ingredient(s) could not be uploaded: Quantity must be a positive number")

    # Test Case 4: Empty ingredient name with valid quantity
    def test_empty_ingredient_name(self):
        result = self.try_add_ingredient("", 3)
        self.assertTrue(result.startswith("Ingredient(s) could not be uploaded: Invalid ingredient name"))

    # Test Case 7: Invalid characters in ingredient name (e.g., special character "!")
    def test_invalid_ingredient_name(self):
        result = self.try_add_ingredient("Amazing!", 3)
        self.assertEqual(result, "Ingredient(s) could not be uploaded: Invalid ingredient name - only letters, numbers, and hyphens allowed")

if __name__ == '__main__':
    unittest.main()
