import React from "react";

const ProfilePage = ({ onLogout }) => {
  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  return (
    <div className="home-page" style={{ textAlign: "center" }}>
      <p>Username: {username}</p>
      <p>No recipes available.</p>
      <button onClick={onLogout} style={{ marginTop: "1rem" }}>
        Logout
      </button>
    </div>
  );
};

export default ProfilePage;
