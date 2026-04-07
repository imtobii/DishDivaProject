import React, { useState } from "react";
import "../App.css";

const SignupPage = ({ onSignupSuccess, onSwitchToLogin }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSignup = () => {
    if (!username || !email || !password || !confirmPassword) {
      setError("All fields are required.");
      return;
    }
    if (!isValidEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }
    if (password.length <= 5) {
      setError("Password must be greater than 5 characters.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    fetch("http://localhost:8000/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((data) => {
            throw new Error(data.error || "Signup failed.");
          });
        }
        return res.json();
      })
      .then((data) => {
        alert(data.message);
        setError(null);
        onSignupSuccess(); // Notify App.js to redirect to login
      })
      .catch((err) => {
        console.error("Signup error:", err);
        setError(err.message || "An unexpected error occurred.");
      });
  };

  return (
    <div className="auth-page">
      <h2>Create Your DishDiva Account</h2>
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
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="auth-input"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        className="auth-input"
        type="password"
        placeholder="Confirm Password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <button className="auth-button" onClick={handleSignup}>
        Sign Up
      </button>
      <button className="auth-link" onClick={onSwitchToLogin}>
        Already have an account? Login
      </button>
    </div>
  );
};

export default SignupPage;
