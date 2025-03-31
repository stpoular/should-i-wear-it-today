// src/components/Profile.js
import React, { useState, useEffect } from "react";
import { getUserProfile } from "../api/api";

function Profile() {
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      getUserProfile(token)
        .then((data) => setUserProfile(data))
        .catch((error) => console.error("Error fetching profile:", error));
    }
  }, []);

  if (!userProfile) {
    return <div>Loading profile...</div>;
  }

  return (
    <div>
      <h2>User Profile</h2>
      <p>Username: {userProfile.username}</p>
      <p>Email: {userProfile.email}</p>
    </div>
  );
}

export default Profile;
