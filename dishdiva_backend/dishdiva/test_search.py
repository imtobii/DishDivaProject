import django
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ensures dishdiva_backend is on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dishdiva.settings")
django.setup()

import unittest
from dishdiva.classes import AuthSystem, RecipeSearch, User, Recipe, Ingredient, Nutrition

class TestRecipeSearch(unittest.TestCase):
    def setUp(self):
        self.auth = AuthSystem()
        self.search = RecipeSearch(self.auth)

        # Clear any existing recipes
        for user in self.auth.predefined_users:
            user.set_recipes([])

        # Add test recipes
        user = self.auth.predefined_users[0]
        lettuce_nutrition = Nutrition(15, 0.2, 2.9, 1.3)
        tomato_nutrition = Nutrition(18, 2.6, 3.9, 0.9)

        salad = Recipe("Awesome Salad", "Healthy")
        salad.add_ingredient(Ingredient("Lettuce", "grams", lettuce_nutrition), 10)
        salad.add_ingredient(Ingredient("Tomato", "pieces", tomato_nutrition), 2)
        user.upload_recipe(salad)


    # Test Case 1: Valid exact match
    def test_valid_exact_search(self):
        results = self.search.search("Awesome Salad")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_title(), "Awesome Salad")

    # Test Case 1: Valid wildcard search
    def test_valid_wildcard_search(self):
        results = self.search.search("Awesome*")
        self.assertGreaterEqual(len(results), 1)

    # Test Case 2: Exceptional short search
    def test_short_search(self):
        results = self.search.search("a")
        self.assertGreaterEqual(len(results), 1)  # Should find "Awesome Salad"

    # Test Case 3: Invalid SQL injection
    def test_invalid_search(self):
        with self.assertRaises(ValueError) as context:
            self.search.search("\"; DROP TABLE *;--")
        self.assertIn("Invalid characters", str(context.exception))

    # Test Case 4: Empty search
    def test_empty_search(self):
        results = self.search.search("")
        self.assertEqual(len(results), 0)

    # Test Case 5: Long search
    def test_long_search(self):
        long_query = "a" * 1001
        with self.assertRaises(ValueError) as context:
            self.search.search(long_query)
        self.assertIn("Search is too long", str(context.exception))

if __name__ == '__main__':
    unittest.main()
