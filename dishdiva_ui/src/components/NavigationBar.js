import React from "react";

const NavigationBar = ({ isLoggedIn, onNavigate }) => (
  <nav className="navbar">
    <div className="nav-left">
      <button className="logo" onClick={() => onNavigate("home")}>DishDiva</button>
    </div>
    <div className="nav-right">
      <button onClick={() => onNavigate("recipes")}>Recipes</button>
      <button onClick={() => onNavigate("ingredients")}>Ingredients</button>
      {isLoggedIn ? (
        <button onClick={() => onNavigate("profile")}>Profile</button>
      ) : (
        <button onClick={() => onNavigate("auth")}>Login</button>
      )}
    </div>
  </nav>
);

export default NavigationBar;