import React from "react";
import "../App.css";

const RecipeCard = ({ recipe, onClick }) => {
  return (
    <div className="recipe-card" onClick={onClick} style={{ cursor: "pointer" }}>
      <div className="recipe-card-content">
        <h3 className="recipe-title">{recipe.name}</h3>
        {recipe.ingredients && recipe.ingredients.length > 0 && (
          <>
            <h4>Ingredients:</h4>
            <ul>
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              ))}
            </ul>
          </>
        )}
        {recipe.category && <p style={{ marginTop: "0.5rem" }}><strong>Type:</strong> {recipe.category}</p>}
      </div>
    </div>
  );
};

export default RecipeCard;