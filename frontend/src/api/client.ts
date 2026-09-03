// A single axios instance that every page uses. It automatically
// attaches the JWT (if we have one) to every request, and points
// at the FastAPI backend running on port 8000.

import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
