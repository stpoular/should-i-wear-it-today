//api/api.js
import axios from "axios";
import { API_URL } from "../config";

// Register a new user
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/users/`, userData);
    return response.data;
  } catch (error) {
    console.error("Registration error:", error.response?.data || error.message);
    throw new Error("Error registering user");
  }
};

// Login user
export const loginUser = async (loginData) => {
  console.log("Login function triggered");
  console.log("Final API URL:", API_URL);
  console.log("Full request URL:", `${API_URL}/tokens/`);

  try {
    const response = await fetch(`${API_URL}/tokens/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginData),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Login error:", error);
    throw new Error("Login failed");
  }
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
  console.log("Updating user with data:", userData); // 🔍 Log what data is being sent

  try {
    const response = await axios.put(`${API_URL}/users/me/`, userData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating user:", error.response?.data || error.message);
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



// Create a new item
export const createItem = async (itemData, token) => {
  try {
    const response = await axios.post(`${API_URL}/items/`, itemData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating item:", error.response?.data || error.message);
    throw new Error("Error creating item");
  }
};

// Get all items
export const getItems = async () => {
  try {
    const response = await axios.get(`${API_URL}/items/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching items:", error.response?.data || error.message);
    throw new Error("Error fetching items");
  }
};

// Get a specific item by ID
export const getItemById = async (itemId) => {
  try {
    const response = await axios.get(`${API_URL}/items/${itemId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching item:", error.response?.data || error.message);
    throw new Error("Error fetching item");
  }
};





// Create a new submission
export const createSubmission = async (submissionData, token) => {
  try {
    const response = await axios.post(`${API_URL}/submissions/`, submissionData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating submission:", error.response?.data || error.message);
    throw new Error("Error creating submission");
  }
};

// Get all submissions for the current user
export const getSubmissionsForUser = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/submissions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching submissions:", error.response?.data || error.message);
    throw new Error("Error fetching submissions");
  }
};

// Get submissions by item ID
export const getSubmissionsForItem = async (itemId) => {
  try {
    const response = await axios.get(`${API_URL}/submissions/?item_id=${itemId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching submissions for item:", error.response?.data || error.message);
    throw new Error("Error fetching submissions for item");
  }
};



