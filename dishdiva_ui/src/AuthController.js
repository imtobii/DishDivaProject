import React, { useState } from "react";
import Login from "./components/LoginPage";
import Signup from "./components/SignupPage";

const AuthController = () => {
  const [activeForm, setActiveForm] = useState("login");

  return activeForm === "login" ? (
    <Login onSwitch={() => setActiveForm("signup")} />
  ) : (
    <Signup onSwitch={() => setActiveForm("login")} />
  );
};

export default AuthController;
