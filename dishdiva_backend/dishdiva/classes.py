from __future__ import annotations

import re
from typing import List

from django.apps import AppConfig

from . import models


class User(AppConfig):
    def __init__(self, username: str, email: str, password: str):
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)

        self.username = username
        self.email = email
        self.password = password
        self.__ingredients = []  # Private list for ingredients
        self.__recipes = []  # Private list for recipes

    # Original ingredient/recipe methods
    def add_ingredient(self, ingredient, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")
        self.__ingredients.append((ingredient, quantity))


    def get_ingredients(self):
        return self.__ingredients.copy()

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def set_recipes(self, recipes):
        self.__recipes = recipes

    def save_recipe(self, recipe):
        self.__recipes.append(recipe)

    def upload_recipe(self, recipe: Recipe) -> str:
        try:
            recipe.validate_recipe()  # Add this line
            self.__recipes.append(recipe)
            return "Recipe uploaded successfully"
        except (ValueError, TypeError) as e:
            return f"Recipe not uploaded: {str(e)}"

    def get_recipes(self):
        return self.__recipes.copy()

    # Validation methods
    def _validate_username(self, username):
        if not re.match(r"^[a-zA-Z0-9_]{5,20}$", username):
            raise ValueError(
                "Username must be 5-20 alphanumeric chars with underscores"
            )

    def _validate_email(self, email):
        if not re.match(r"^\w+@\w+\.\w+$", email):
            raise ValueError("Invalid email format")

    def _validate_password(self, password):
        if len(password) < 8 or len(password) > 20:
            raise ValueError("Password must be 8-20 characters")
        if not any(c.isalpha() for c in password):
            raise ValueError("Password must contain at least one letter")

    # Storage methods
    def store_user(self):
        usr = models.User(name=self.username, email=self.email, password=self.password)
        usr.save()

        for ingredient, quantity in self.__ingredients:
            ing = ingredient.store_ingredient()
            ingr = models.Ingredients(ingredient=ing, quantity=quantity)
            ingr.save()
            usr.ingredients.add(ingr)

            for recipe in self.__recipes:
                rec = recipe.store_recipe()
                usr.recipes.add(rec)
        return usr

    def store_recipes(self):
        stored = []
        for recipe in self.__recipes:
            rec = recipe.store_recipe()
            rec.save()
            stored.append(rec)
        return stored

    def fetch_recipes(self):
        usr = models.User.objects.get(email=self.email)
        recipes = usr.recipes.all()
        self.__recipes = [
            Recipe.fetch_recipe(r) for r in recipes
        ]  # Assumes this method exists

    def store_ingredients(self):
        stored = []
        for ingredient, quantity in self.__ingredients:
            ing = ingredient.store_ingredient()
            ingr = models.Ingredients(ingredient=ing, quantity=quantity)
            ingr.save()
            stored.append(ingr)
        return stored

    def fetch_ingredients(self):
        usr = models.User.objects.get(email=self.email)
        ingr_links = usr.ingredients.all()
        fetched = []
        for ing_link in ingr_links:
            ingredient_model = ing_link.ingredient
            logic_obj = Ingredient.fetch_ingredients(ingredient_model.id)
            fetched.append((logic_obj, ing_link.quantity))
        self.__ingredients = fetched

    def fetch_user(db_id):
        usr = User(db_id.name, db_id.email, db_id.password)
        usr.fetch_ingredients()
        usr.fetch_recipes()
        return usr


class AuthSystem(AppConfig):
    predefined_users = [
        User("meowmeow", "meow@realwebsites.com", "m30wm30w$"),
        User("chipchip", "chip@realwebsites.com", "ch1pch1p$"),
    ]

    def __init__(self):
        self.users = {user.email: user for user in self.predefined_users}
        self.current_user = None

    def login(self, identifier: str, password: str) -> bool:
        user = next(
            (
                u
                for u in self.predefined_users
                if u.email == identifier or u.username == identifier
            ),
            None,
        )
        if user and user.password == password:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None


class Ingredient(AppConfig):
    def __init__(self, name, unit, nutrition):
        if not re.match(r"^[a-zA-Z0-9 \-]+$", name):
            raise ValueError(
                "Invalid ingredient name - only letters, numbers, and hyphens allowed"
            )
        self.__name = name
        self.__unit = unit  # also units for  how we measure quantity(cup, lb, g, etc.)
        self.__nutrition = nutrition

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_unit(self, unit):
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def set_unit(self, unit):
        self.__unit = unit

    def get_nutrition(self):
        return self.__nutrition

    def set_nutrition(self, nutr):
        self.__nutrition = nutr

    def store_ingredient(self):
        nutr = store_nutrition(self.__nutrition)
        ingr = models.Ingredient(name=self.__name, quantity=self.__unit, nutrition=nutr)
        ingr.save()
        return ing

    def fetch_ingredient(ingr_id):
        return Ingredient(
            ingr.name, ingr.quantity, Nutrition.fetch_nutrition(ingr.nutrition)
        )


class Nutrition(AppConfig):
    def __init__(self, calories, sugars, carbs, protein):
        self.__calories = calories
        self.__sugars = sugars
        self.__carbs = carbs
        self.__protein = protein

    def set_calories(self, calories):
        self.__calories = calories

    def get_calories(self):
        return self.__calories

    def set_sugars(self, sugars):
        self.__sugars = sugars

    def get_sugars(self):
        return self.__sugars

    def set_carbs(self, carbs):
        self.__carbs = carbs

    def get_carbs(self):
        return self.__carbs

    def set_protein(self, protein):
        self.__protein = protein

    def get_protein(self):
        return self.__protein

    def store_nutrition(self):
        nutrition = models.Nutrition(
            calories=self.__calories,
            carbs=self.__carbs,
            sugars=self.__sugars,
            protein=self.__protein,
        )
        nutrition.save()
        return nutrition

    def fetch_nutrition(nutr_id):
        return Nutrition(
            nutr_id.calories, nutr_id.sugars, nutr_id.carbs, nutr_id.protein
        )


class Recipe(AppConfig):
    VALID_CATEGORIES = {
        "Healthy",
        "Vegetarian",
        "Vegan",
        "GlutenFree",
    }  # Customize as needed

    def __init__(self, title: str, category: str, instructions: str = ""):
        self._validate_title(title)
        self._validate_category(category)
        self.__title = title
        self.__category = category
        self.__ingredients = {}
        self.__instructions = instructions

    def validate_recipe(self):
        if not self.__ingredients:
            raise ValueError("At least one ingredient required")

    # Validation methods
    def _validate_title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not re.match(r"^[a-zA-Z0-9 ]+$", title):
            raise ValueError(
                "Title must contain only alphanumeric characters and spaces"
            )
        if not title.strip():
            raise ValueError("Title cannot be empty")

    def _validate_category(self, category):
        if not isinstance(category, str):
            raise TypeError("Category must be a string")
        if not re.match(r"^[a-zA-Z0-9 ]+$", category):
            raise ValueError(
                "Invalid category format - only alphanumeric and spaces allowed"
            )
        if not category.strip():
            raise ValueError("Category cannot be empty")
        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category. Valid options: {', '.join(self.VALID_CATEGORIES)}"
            )

    # Ingredient management
    def add_ingredient(self, ingredient: Ingredient, quantity: float):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")  # Exact message
        self.__ingredients[ingredient] = quantity

    # Nutrition calculation
    def get_nutrition(self) -> "Nutrition":
        total = Nutrition("Total Nutrition", 0, 0, 0, 0)

        for ingredient, quantity in self.__ingredients.items():
            nutrition = ingredient.get_nutrition()
            total.set_calories(
                total.get_calories() + (nutrition.get_calories() * quantity)
            )
            total.set_sugars(total.get_sugars() + (nutrition.get_sugars() * quantity))
            total.set_carbs(total.get_carbs() + (nutrition.get_carbs() * quantity))
            total.set_protein(
                total.get_protein() + (nutrition.get_protein() * quantity)
            )

        return total

    # Getters and setters
    def get_title(self):
        return self.__title

    def set_title(self, title: str):
        self._validate_title(title)
        self.__title = title

    def get_category(self):
        return self.__category

    def set_category(self, category: str):
        self._validate_category(category)
        self.__category = category

    def get_ingredients(self):
        return self.__ingredients.copy()

    def set_ingredients(self, ingredients: dict):
        self.__ingredients = {}
        for ingredient, quantity in ingredients.items():
            self.add_ingredient(ingredient, quantity)

    def get_instructions(self):
        return self.__instructions

    def set_instructions(self, instructions: str):
        self.__instructions = instructions

    def __str__(self):
        return f"{self.__title} ({self.__category}) - {len(self.__ingredients)} ingredients"

    def store_recipe(self):
        recipe = models.Recipe(
            name=self.__title,
            category=self.__category,
            instructions=self.__instructions,
            ingredients=self.ingredients,
        )
        recipe.save()
        return recipe

    def fetch_recipe(recp):
        return recipe(recp.name, recp.category, recp.instructions)

class RecipeSearch:
    def __init__(self, auth_system: AuthSystem):
        self.auth_system = auth_system

    def search(self, query: str) -> List[Recipe]:
        if not isinstance(query, str):
            raise ValueError("Search query must be a string")
        if len(query) > 1000:
            raise ValueError("Search is too long")
        if any(c in query for c in [';', '"', "'"]):
            raise ValueError("Invalid characters in search query")

        # Remove wildcard character for partial matching
        cleaned_query = query.lower().replace("*", "").strip()

        all_recipes = []
        for user in self.auth_system.predefined_users:
            all_recipes.extend(user.get_recipes())

        if not cleaned_query:
            return []

        return [
            recipe for recipe in all_recipes
            if cleaned_query in recipe.get_title().lower()
        ]
