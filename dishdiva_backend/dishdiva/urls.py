"""
URL configuration for dishdiva project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from . import calls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("recipe/<str:recipe_id>/", calls.recipe, name = "recipe"),
    path("user/<str:user_id>/", calls.user, name = "user"),
    path("ingredient/<str:ingredient_id>/", calls.ingredient, name = "ingredient"),
    path("ingredients/", calls.ingredients_list, name="ingredients_list"),
    # path("search/<str:search_request>/", calls.search, name = "search"),
    path("searchRecipe/<str:search_request>/", calls.searchRecipe, name="searchRecipe"),
    path('calls/recipes/', calls.all_recipes, name='all_recipes'),
    path("searchUser/<str:search_request>/", calls.getUserFromDb, name="getUserFromDb"),
    path("login/", calls.login, name="login"),
    path('signup/', calls.signup, name='signup'),
    path("update_profile/", calls.update_profile, name="update_profile"),
    path("get_user/<int:user_id>/", calls.get_user, name="get_user"),
    path("calls/add_recipe/", calls.add_recipe, name="add_recipe"),
    # path('ingredients/', calls.get_ingredients, name='get_ingredients'),
    # path('ingredients/add/', calls.add_ingredient, name='add_ingredient'),
    path("user/<int:user_id>/recipes/", calls.user_recipes, name="user_recipes"),

]
