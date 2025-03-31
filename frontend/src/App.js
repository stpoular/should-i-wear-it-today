// src/App.js

import axios from "axios";  // This should be at the top
import { useState } from "react";  // This should be at the top
import Header from "./components/Header";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";

console.log("Process.env:", process.env);

const API_URL = process.env.REACT_APP_API_URL || "http://34.138.45.167:8000";
console.log("API URL (api.js):", API_URL); // Debug log

function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="App">
      <Header />
      {page === "home" && (
        <div>
          <button onClick={() => setPage("login")}>Login</button>
          <button onClick={() => setPage("register")}>Register</button>
        </div>
      )}
      {page === "login" && <Login />}
      {page === "register" && <Register />}
      {page === "profile" && <Profile />}
    </div>
  );
}

export default App;






// Register a new user
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/users/`, userData);
    return response.data;
  } catch (error) {
    console.error("Registration error:", error.response ? error.response.data : error.message);
    throw new Error("Error registering user");
  }
};



export const loginUser = async (loginData) => {
  console.log("Login function triggered");
  console.log("Final API URL:", API_URL);
  console.log("Full request URL:", `${API_URL}/tokens/`);


  //const response = await fetch(`${API_URL}/tokens/`, {
  const response = await fetch(`http://34.138.45.167:8000/tokens/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(loginData),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  return await response.json();
};







// Get the details of the current authenticated user
export const getCurrentUser = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/users/me/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error("Error fetching user details");
  }
};

// Update user details
export const updateUser = async (userData, token) => {
  try {
    const response = await axios.put(`${API_URL}/users/me/`, userData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error("Error updating user details");
  }
};

// Delete user account
export const deleteUser = async (token) => {
  try {
    const response = await axios.delete(`${API_URL}/users/me/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error("Error deleting user");
  }
};
