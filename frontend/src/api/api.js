// src/api/api.js
import axios from "axios";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${backendUrl}/users/`, userData);
    return response.data;
  } catch (error) {
    console.error("Error registering user:", error);
    throw error;
  }
};

export const loginUser = async (loginData) => {
  try {
    const response = await axios.post(`${backendUrl}/tokens/`, loginData);
    return response.data;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

export const getUserProfile = async (token) => {
  try {
    const response = await axios.get(`${backendUrl}/users/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
};

export const updateUserProfile = async (userData, token) => {
  try {
    const response = await axios.put(`${backendUrl}/users/me/`, userData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating user profile:", error);
    throw error;
  }
};
