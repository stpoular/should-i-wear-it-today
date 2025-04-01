// src/components/Login.js
import React, { useState } from "react";
import { loginUser } from "../api/api";

function Login({ onLoginSuccess }) {  // ⬅️ Accept function from App.js
  const [loginData, setLoginData] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(loginData);
      localStorage.setItem("token", data.access_token);
      alert("Login successful!");
      onLoginSuccess();  // ⬅️ Tell App.js to go to Profile page
    } catch (error) {
      console.error("Login error:", error);
      alert("Error logging in");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Username" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
