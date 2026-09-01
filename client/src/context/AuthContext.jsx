// src/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect, useCallback } from "react";

const AuthContext = createContext(null);

export function useAuthContext() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  // Load user profile if token exists
  useEffect(() => {
    if (!token) return;

    async function fetchProfile() {
      try {
        const res = await fetch("/api/user", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.ok) {
          const data = await res.json();
          setUser(data);
        } else {
          localStorage.removeItem("token");
          setToken(null);
          setUser(null);
        }
      } catch {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      }
    }

    fetchProfile();
  }, [token]);

  const login = useCallback((tokenValue, userData) => {
    localStorage.setItem("token", tokenValue);
    setToken(tokenValue);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    token,
    isAuthenticated: Boolean(token),
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}


