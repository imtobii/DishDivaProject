import React, { useEffect, useState } from "react";
import "../App.css";

const Ingredients = ({ onNavigate }) => {
  const [ingredients, setIngredients] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/ingredients/")
      .then(response => response.json())
      .then(data => setIngredients(data))
      .catch(error => console.error("Error fetching ingredients:", error));
  }, []);

  return (
    <div className="page-container">
      <button
        className="update-button"
        onClick={() => onNavigate("update-ingredients")}
      >
        Update Ingredients
      </button>

      <table className="ingredients-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Quantity</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map((ingredient, index) => (
            <tr key={index}>
              <td>{ingredient.name}</td>
              <td>{ingredient.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Ingredients;
