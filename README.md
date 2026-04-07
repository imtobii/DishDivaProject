# DishDiva

A full-stack recipe management web application that lets users discover recipes, manage their ingredient pantry, and create their own recipes.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 |
| Backend | Django 5.1 |
| Database | SQLite |

## Features

- **User accounts** — sign up, log in, and manage your profile
- **Recipe browser** — browse all recipes or search by name
- **Recipe categories** — Generic, Healthy, Vegetarian, Vegan, Gluten-Free
- **Create recipes** — add your own recipes with ingredients and instructions
- **Ingredient pantry** — track ingredients with quantity and nutrition info (calories, carbs, protein, sugars)
- **User recipe collection** — save and view recipes tied to your account

## Project Structure

```
DishDivaProject/
├── dishdiva_backend/     # Django REST backend
│   └── dishdiva/
│       ├── models.py     # AppUser, Recipe, Ingredient, Nutrition models
│       ├── calls.py      # API view functions
│       ├── urls.py       # URL routing
│       └── settings.py
└── dishdiva_ui/          # React frontend
    └── src/
        └── components/   # LoginPage, SignupPage, HomePage, RecipePage,
                          # RecipeCard, RecipeDetail, IngredientsPage,
                          # ProfilePage, NavigationBar, UpdateIngredients
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login/` | Authenticate a user |
| POST | `/signup/` | Register a new user |
| POST | `/update_profile/` | Update username / profile picture |
| GET | `/get_user/<user_id>/` | Get user info |
| GET | `/calls/recipes/` | List all recipes |
| GET | `/recipe/<recipe_id>/` | Get a single recipe |
| POST | `/calls/add_recipe/` | Create a new recipe |
| GET | `/user/<user_id>/recipes/` | Get recipes saved by a user |
| GET | `/searchRecipe/<query>/` | Search recipes by name |
| GET | `/ingredients/` | List all ingredients |
| POST | `/ingredients/` | Add a new ingredient |
| GET/PUT/DELETE | `/ingredient/<ingredient_id>/` | Get, update, or delete an ingredient |

## Getting Started

### Backend

```bash
cd dishdiva_backend
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd dishdiva_ui
npm install
npm start
```

The app will open at `http://localhost:3000`.

## License

See [LICENSE](LICENSE).
