// src/components/Profile.js
import React, { useState, useEffect } from "react";
import { getCurrentUser, updateUser } from "../api/api";

function Profile() {
  const [userProfile, setUserProfile] = useState({
    username: "",
    email: "",
    password: "", // Include a password field
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      getCurrentUser(token)
        .then((data) => setUserProfile({ username: data.username, email: data.email, password: "" })) // Don't include password
        .catch((error) => console.error("Error fetching profile:", error));
    }
  }, []);

  const handleChange = (e) => {
    setUserProfile({ ...userProfile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("token");

  try {
    const updateData = {};
    if (userProfile.password) {
      updateData.password = userProfile.password; // Only send password if it has changed
    }
    console.log("Submitting update:", updateData);  // Log the data being sent

    await updateUser(updateData, token);
    alert("Password updated successfully!");
  } catch (error) {
    console.error("Error updating profile:", error);
    alert("Failed to update profile.");
  }
};


  return (
    <div>
      <h2>User Profile</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={userProfile.username} disabled />
        </label>
        <label>
          Email:
          <input type="email" name="email" value={userProfile.email} disabled />
        </label>
        <label>
          New Password:
          <input type="password" name="password" value={userProfile.password} onChange={handleChange} />
        </label>
        <button type="submit">Update Password</button>
      </form>
    </div>
  );
}

export default Profile;
