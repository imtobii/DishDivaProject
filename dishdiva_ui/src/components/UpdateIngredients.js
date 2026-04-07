/*import React, { useState } from "react";

const UpdateIngredients = () => {
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [calories, setCalories] = useState("");
  const [sugars, setSugars] = useState("");
  const [carbs, setCarbs] = useState("");
  const [protein, setProtein] = useState("");

  const handleAdd = () => {
    const ingredient = {
      name,
      quantity,
      nutrition: {
        calories: parseFloat(calories),
        sugars: parseFloat(sugars),
        carbs: parseFloat(carbs),
        protein: parseFloat(protein),
      }
    };

    fetch("http://localhost:8000/ingredients/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ingredient),
    })
      .then(res => res.json())
      .then(data => {
        alert("Ingredient added: " + data.message);
        setName(""); setQuantity("");
        setCalories(""); setSugars(""); setCarbs(""); setProtein("");
      })
      .catch(error => console.error("Error adding ingredient:", error));
  };

  return (
    <div>
      <div className="main update">
        <div className="left-section">
          <div className="section-title">Insert Ingredients</div>
          <div className="input-group">
            <label>Ingredient name</label>
            <input value={name} onChange={e => setName(e.target.value)} type="text" placeholder="e.g. Sugar" />
          </div>
          <div className="input-group">
            <label>Ingredient quantity</label>
            <input value={quantity} onChange={e => setQuantity(e.target.value)} type="text" placeholder="e.g. 2 cups" />
          </div>
          <div className="input-group">
            <label>Calories</label>
            <input value={calories} onChange={e => setCalories(e.target.value)} type="number" />
          </div>
          <div className="input-group">
            <label>Sugars</label>
            <input value={sugars} onChange={e => setSugars(e.target.value)} type="number" />
          </div>
          <div className="input-group">
            <label>Carbs</label>
            <input value={carbs} onChange={e => setCarbs(e.target.value)} type="number" />
          </div>
          <div className="input-group">
            <label>Protein</label>
            <input value={protein} onChange={e => setProtein(e.target.value)} type="number" />
          </div>
          <button className="add-btn" onClick={handleAdd}>Add Ingredient</button>

          <div className="section-title">Edit Ingredients</div>
          <div className="edit-list">
            {["Sugar - 2 cups", "Flour - 1.5 cups", "Salt - 1 tsp"].map(
              (item, index) => (
                <div className="ingredient-row" key={index}>
                  {item}
                  <div className="action-buttons">
                    <button className="edit-btn">✎</button>
                    <button className="delete-btn">×</button>
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UpdateIngredients;
*/

import React, { useState, useEffect } from "react";

const UpdateIngredients = () => {
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [calories, setCalories] = useState("");
  const [sugars, setSugars] = useState("");
  const [carbs, setCarbs] = useState("");
  const [protein, setProtein] = useState("");
  const [ingredients, setIngredients] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const fetchIngredients = () => {
    fetch("http://localhost:8000/ingredients/")
      .then((res) => res.json())
      .then((data) => setIngredients(data))
      .catch((err) => console.error("Fetch error:", err));
  };

  useEffect(() => {
    fetchIngredients();
  }, []);

  const handleAddOrUpdate = () => {
    const ingredient = {
      name,
      quantity,
      nutrition: {
        calories: parseFloat(calories),
        sugars: parseFloat(sugars),
        carbs: parseFloat(carbs),
        protein: parseFloat(protein),
      },
    };

    const url = editingId
      ? `http://localhost:8000/ingredient/${editingId}/`
      : "http://localhost:8000/ingredients/";

    const method = editingId ? "PUT" : "POST";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ingredient),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(`Ingredient ${editingId ? "updated" : "added"}: ` + data.message);
        setName("");
        setQuantity("");
        setCalories("");
        setSugars("");
        setCarbs("");
        setProtein("");
        setEditingId(null);
        fetchIngredients();
      })
      .catch((error) => console.error("Error submitting ingredient:", error));
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setName(item.name);
    setQuantity(item.quantity);
    setCalories(item.nutrition?.calories || "");
    setSugars(item.nutrition?.sugars || "");
    setCarbs(item.nutrition?.carbs || "");
    setProtein(item.nutrition?.protein || "");
  };

  const handleDelete = (id) => {
    fetch(`http://localhost:8000/ingredient/${id}/`, {
      method: "DELETE",
    })
      .then(() => {
        alert("Ingredient deleted");
        fetchIngredients();
      })
      .catch((error) => console.error("Error deleting ingredient:", error));
  };

  return (
    <div className="page-container">
      <div className="main update">
        <div className="left-section">
          <h2 className="section-title">Manage Ingredients</h2>

          <div className="form-grid even-inputs">
            <div className="input-group">
              <label>Ingredient Name:</label>
              <input value={name} onChange={(e) => setName(e.target.value)} type="text" placeholder="e.g. Sugar" />
            </div>
            <div className="input-group">
              <label>Quantity:</label>
              <input value={quantity} onChange={(e) => setQuantity(e.target.value)} type="text" placeholder="e.g. 2 cups" />
            </div>
            <div className="input-group">
              <label>Calories:</label>
              <input value={calories} onChange={(e) => setCalories(e.target.value)} type="number" />
            </div>
            <div className="input-group">
              <label>Sugars:</label>
              <input value={sugars} onChange={(e) => setSugars(e.target.value)} type="number" />
            </div>
            <div className="input-group">
              <label>Carbs:</label>
              <input value={carbs} onChange={(e) => setCarbs(e.target.value)} type="number" />
            </div>
            <div className="input-group">
              <label>Protein:</label>
              <input value={protein} onChange={(e) => setProtein(e.target.value)} type="number" />
            </div>
          </div>
          <button className="add-btn" onClick={handleAddOrUpdate}>
            {editingId ? "Update Ingredient" : "Add Ingredient"}
          </button>

          <h3 className="section-title">Existing Ingredients</h3>

          <table className="ingredients-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Quantity</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {ingredients.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{item.quantity}</td>
                  <td>
                    <button className="edit-btn" onClick={() => handleEdit(item)}>✎ Edit</button>
                    <button className="delete-btn" onClick={() => handleDelete(item.id)}>x Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UpdateIngredients;
