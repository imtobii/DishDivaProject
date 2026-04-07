import React, { useState } from "react";
import "../App.css";

const LoginPage = ({ onLogin, onSwitchToSignup }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = () => {
    fetch("http://localhost:8000/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: username, password }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((data) => {
            throw new Error(data.message || "Login failed.");
          });
        }
        return res.json();
      })
      .then((data) => {
        alert(data.message);
        setError(null);

        // Save userId and username to localStorage
        localStorage.setItem("userId", data.userId);
        localStorage.setItem("username", data.username);
        

        onLogin();
      })
      .catch((err) => {
        console.error("Login error:", err);
        setError(err.message || "An unexpected error occurred.");
      });
  };

  return (
    <div className="auth-page">
      <h2>Login to DishDiva</h2>
      {error && <p className="error-message">{error}</p>}
      <input
        className="auth-input"
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="auth-input"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="auth-button" onClick={handleLogin}>
        Login
      </button>
      <button className="auth-link" onClick={onSwitchToSignup}>
        Don't have an account? Sign up
      </button>
    </div>
  );
};

export default LoginPage;
