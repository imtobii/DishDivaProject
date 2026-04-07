import React from "react";

const RecipeDetail = ({ recipe, onBack }) => {
  if (!recipe) {
    return (
      <div className="page-container">
        <button className="back-button" onClick={onBack}>← Back</button>
        <p>No recipe selected.</p>
      </div>
    );
  }

  return (
    <div className="page-container">
      <button className="back-button" onClick={onBack}>← Back</button>
      <h2>{recipe.name}</h2>

      {recipe.ingredients.length > 0 && (
        <>
          <h4>Ingredients:</h4>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
        </>
      )}

      {recipe.instructions && (
        <>
          <h4>Instructions:</h4>
          <p>{recipe.instructions}</p>
        </>
      )}

      {recipe.category && <p style={{ fontStyle: "italic" }}>Type: {recipe.category}</p>}
    </div>
  );
};

export default RecipeDetail;