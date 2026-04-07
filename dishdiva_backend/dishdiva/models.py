from django.db import models
from django.contrib.auth.models import AbstractUser

class Nutrition(models.Model):
    calories = models.IntegerField(default=0)
    sugars = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=20)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)

class Ingredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)

class Recipe(models.Model):
    CATEGORIES = [
        ("Generic", "Generic"),
        ("Healthy", "Healthy"),
        ("Vegetarian", "Vegetarian"),
        ("Vegan", "Vegan"),
        ("GlutenFree", "GlutenFree"),
    ]


    name = models.CharField(max_length=200)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    instructions = models.CharField(max_length=200000)
    ingredients = models.ManyToManyField(Ingredients)

class AppUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredients)
    recipes = models.ManyToManyField(Recipe)
