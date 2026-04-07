import React, { useState } from "react";
import './App.css';
import NavigationBar from "./components/NavigationBar";
import HomePage from "./components/HomePage";
import RecipeDetail from "./components/RecipeDetail";
import ProfilePage from "./components/ProfilePage";
import RecipesPage from "./components/RecipePage";
import IngredientsPage from "./components/IngredientsPage";
import UpdateIngredientsPage from "./components/UpdateIngredients";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";

const App = () => {
  const [activePage, setActivePage] = useState("auth"); // Default to login page
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login state

  const handleLogin = () => {
    setIsLoggedIn(true);
    setActivePage("home"); // Redirect to profile after login
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setActivePage("auth"); // Redirect to login page after logout
  };

  const handleSignupSuccess = () => {
    setActivePage("auth"); // Redirect to login page after successful signup
  };

  const renderPage = () => {
    if (selectedRecipe) return <RecipeDetail recipe={selectedRecipe} onBack={() => setSelectedRecipe(null)} />;
  
    switch (activePage) {
      case "home":
        return <HomePage onRecipeSelect={(recipe) => setSelectedRecipe(recipe)} />;
      case "recipes":
        return <RecipesPage onRecipeSelect={(recipe) => setSelectedRecipe(recipe)} />;
      case "ingredients":
        return <IngredientsPage onNavigate={setActivePage} />;
      case "update-ingredients":
        return <UpdateIngredientsPage />;
      case "profile":
        return <ProfilePage onLogout={handleLogout} />;
      case "auth":
        return (
          <LoginPage
            onLogin={handleLogin}
            onSwitchToSignup={() => setActivePage("signup")}
          />
        );
      case "signup":
        return (
          <SignupPage
            onSignupSuccess={handleSignupSuccess}
            onSwitchToLogin={() => setActivePage("auth")}
          />
        );
      default:
        return <HomePage onRecipeSelect={setSelectedRecipe} />;
    }
  };
  

  return (
    <div>
      {isLoggedIn && <NavigationBar isLoggedIn={isLoggedIn} onNavigate={setActivePage} />} {/* Pass isLoggedIn to NavigationBar */}
      {renderPage()}
    </div>
  );
};

export default App;
