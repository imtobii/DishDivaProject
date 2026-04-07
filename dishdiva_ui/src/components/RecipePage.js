import React, { useEffect, useState } from "react";
import "../App.css";

const RecipePage = () => {
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState(null);
  const [newRecipe, setNewRecipe] = useState({ name: "", category: "", ingredients: [], instructions: "" });
  const [ingredientInput, setIngredientInput] = useState("");
  const [addError, setAddError] = useState(null);

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    if (!userId) {
      setError("User not logged in.");
      return;
    }

    fetch(`http://localhost:8000/user/${userId}/recipes/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => setRecipes(data.results || []))
      .catch((error) => {
        console.error("Error fetching recipes:", error);
        setError("No recipes available");
      });
  }, [userId]);

  const handleAddRecipe = (e) => {
    e.preventDefault();

    if (!newRecipe.name || !newRecipe.category || newRecipe.ingredients.length === 0) {
      setAddError("Name, category, and at least one ingredient are required.");
      return;
    }

    fetch("http://localhost:8000/calls/add_recipe/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...newRecipe, user_id: userId }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to add recipe.");
        }
        return response.json();
      })
      .then((data) => {
        setRecipes((prevRecipes) => [...prevRecipes, data]);
        setNewRecipe({ name: "", category: "", ingredients: [], instructions: "" });
        setIngredientInput("");
        setAddError(null);
      })
      .catch((error) => {
        console.error("Error adding recipe:", error);
        setAddError("Failed to add recipe. Please try again later.");
      });
  };

  const handleAddIngredient = () => {
    if (ingredientInput.trim() === "") return;

    setNewRecipe((prevRecipe) => ({
      ...prevRecipe,
      ingredients: [...prevRecipe.ingredients, ingredientInput.trim()],
    }));
    setIngredientInput("");
  };

  const handleRemoveIngredient = (index) => {
    setNewRecipe((prevRecipe) => ({
      ...prevRecipe,
      ingredients: prevRecipe.ingredients.filter((_, i) => i !== index),
    }));
  };

  return (
    <div className="page-container">
      <h1>My Recipes</h1>

      <div className="add-recipe-form" style={{ marginBottom: "2rem" }}>
        <h2>Add a New Recipe</h2>
        <form onSubmit={handleAddRecipe}>
          <input
            type="text"
            placeholder="Recipe Name"
            value={newRecipe.name}
            onChange={(e) => setNewRecipe({ ...newRecipe, name: e.target.value })}
            style={{ marginRight: "1rem", padding: "0.5rem" }}
          />
          <select
            value={newRecipe.category}
            onChange={(e) => setNewRecipe({ ...newRecipe, category: e.target.value })}
            style={{ marginRight: "1rem", padding: "0.5rem" }}
          >
            <option value="">Select Category</option>
            <option value="Generic">Generic</option>
            <option value="Healthy">Healthy</option>
            <option value="Vegetarian">Vegetarian</option>
            <option value="Vegan">Vegan</option>
            <option value="GlutenFree">GlutenFree</option>
          </select>

          <div style={{ marginTop: "1rem" }}>
            <input
              type="text"
              placeholder="Add Ingredient"
              value={ingredientInput}
              onChange={(e) => setIngredientInput(e.target.value)}
              style={{ marginRight: "1rem", padding: "0.5rem" }}
            />
            <button type="button" onClick={handleAddIngredient} style={{ padding: "0.5rem 1rem" }}>
              Add Ingredient
            </button>
          </div>

          <ul style={{ marginTop: "1rem" }}>
            {newRecipe.ingredients.map((ingredient, index) => (
              <li key={index} style={{ marginBottom: "0.5rem" }}>
                {ingredient}
                <button
                  type="button"
                  onClick={() => handleRemoveIngredient(index)}
                  style={{
                    marginLeft: "1rem",
                    padding: "0.2rem 0.5rem",
                    backgroundColor: "red",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer",
                  }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>

          <textarea
            placeholder="Enter instructions here..."
            value={newRecipe.instructions}
            onChange={(e) => setNewRecipe({ ...newRecipe, instructions: e.target.value })}
            style={{ width: "100%", marginTop: "1rem", padding: "0.5rem", minHeight: "100px" }}
          ></textarea>

          <button type="submit" style={{ marginTop: "1rem", padding: "0.5rem 1rem" }}>
            Add Recipe
          </button>
        </form>
        {addError && <p style={{ color: "red" }}>{addError}</p>}
      </div>

      {error ? (
        <p>{error}</p>
      ) : recipes.length > 0 ? (
        <div className="recipe-list">
          {recipes.map((recipe) => (
            <div key={recipe.id} className="recipe-item" style={{ marginBottom: "1rem" }}>
              <h2>{recipe.name}</h2>
              <p><strong>Category:</strong> {recipe.category}</p>
              <p><strong>Ingredients:</strong> {recipe.ingredients.join(", ")}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No recipes available. Please check back later.</p>
      )}
    </div>
  );
};

export default RecipePage;
