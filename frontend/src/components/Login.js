// src/components/Login.js
import React, { useState } from "react";
import { loginUser } from "../api/api";
import { API_URL } from "../config"; // Import the API URL

function Login() {
  const [loginData, setLoginData] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLoginData({ ...loginData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting login data:", loginData);
    console.log("Login function triggered");
    console.log("Final API URL:", API_URL); // Log the API URL here
    console.log("Full request URL:", `${API_URL}/tokens/`);

    try {
      const response = await fetch(`${API_URL}/tokens/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginData),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");
      } else {
        alert("Error logging in");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      alert("Error logging in");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
