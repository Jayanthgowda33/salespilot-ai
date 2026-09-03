// Keeps track of whether someone is logged in, and exposes login()
// / logout() / signup() to the rest of the app. The token itself
// lives in localStorage so a page refresh doesn't log you out.

import React, { createContext, useContext, useState } from "react";
import { api } from "../api/client";

interface AuthContextType {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (companyName: string, fullName: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  async function login(email: string, password: string) {
    // FastAPI's OAuth2PasswordRequestForm expects form-encoded data,
    // not JSON, with the field named "username" for the email.
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);

    const res = await api.post("/api/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    localStorage.setItem("token", res.data.access_token);
    setToken(res.data.access_token);
  }

  async function signup(companyName: string, fullName: string, email: string, password: string) {
    const res = await api.post("/api/auth/signup", {
      company_name: companyName,
      full_name: fullName,
      email,
      password,
    });
    localStorage.setItem("token", res.data.access_token);
    setToken(res.data.access_token);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
