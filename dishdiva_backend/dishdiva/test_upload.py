import django
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ensures dishdiva_backend is on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dishdiva.settings")
django.setup()

import unittest
from dishdiva.classes import Recipe, Ingredient, Nutrition, User

class TestRecipeUpload(unittest.TestCase):
    def setUp(self):
        self.lettuce_nutrition = Nutrition(15, 0.2, 2.9, 1.3)
        self.tomato_nutrition = Nutrition(18, 2.6, 3.9, 0.9)
        self.lettuce = Ingredient("Lettuce", "grams", self.lettuce_nutrition)
        self.tomato = Ingredient("Tomato", "pieces", self.tomato_nutrition)
        self.user = User("chef123", "chef@cooking.com", "ValidPass123!")

    def _create_recipe(self, title, category, ingredients):
        try:
            recipe = Recipe(title, category)
            for ingredient, quantity in ingredients:
                recipe.add_ingredient(ingredient, quantity)
            return self.user.upload_recipe(recipe)
        except (ValueError, TypeError) as e:
            return f"Recipe not uploaded: {str(e)}"

    # Test Case 1: Valid recipe
    def test_valid_recipe_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, 2.0)]
        result = self._create_recipe("Awesome Salad", "Healthy", ingredients)
        self.assertEqual(result, "Recipe uploaded successfully")

    # Test Case 2: Malicious quantity
    def test_malicious_quantity_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, -2.0)]
        result = self._create_recipe("Test Recipe", "Healthy", ingredients)
        self.assertIn("Quantity must be a positive number", result)

    # Test Case 3: Empty ingredients
    def test_empty_ingredients_upload(self):
        result = self._create_recipe("Empty Salad", "Healthy", [])
        self.assertIn("At least one ingredient required", result)

    # Test Case 4: Invalid category
    def test_invalid_category_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, 2.0)]
        result = self._create_recipe("Awesome Salad", "Unhealthy", ingredients)
        self.assertIn("Invalid category. Valid options", result)

    # Test Case 7: Empty category
    def test_empty_category_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, 2.0)]
        result = self._create_recipe("Awesome Salad", " ", ingredients)
        self.assertIn("Category cannot be empty", result)

    # Test Case 10: Invalid title
    def test_invalid_title_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, 2.0)]
        result = self._create_recipe("Salad!!!!!!!$('I@$*';", "Healthy", ingredients)
        self.assertIn("Title must contain only alphanumeric", result)

    # Test Case 19: Empty title
    def test_empty_title_upload(self):
        ingredients = [(self.lettuce, 10.0), (self.tomato, 2.0)]
        result = self._create_recipe(" ", "Healthy", ingredients)
        self.assertIn("Title cannot be empty", result)

if __name__ == '__main__':
    unittest.main()