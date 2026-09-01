// src/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser, login, signup } from "../services/authService";

const AuthContext = createContext(null);

export function useAuthContext() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user profile if token exists
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      setLoading(false)
      setUser(null)
      return
    }
    getCurrentUser()
      .then((data)=> setUser(data))
      .catch(()=> {
        localStorage.removeItem('token')
        setUser(null)
      })
      .finally( () => setLoading(false))
  }, []);

  async function authenticateUser(credentials) {
    const data = await login(credentials)
    localStorage.setItem("token", data.token);
    setUser(data.user)
    return data.user
  }

  async function createUser(newUser) {
    const data = await signup(newUser)
    localStorage.setItem("token", data.token);
    setUser(data.user)
  }

  async function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{user, loading, authenticateUser, createUser, logout}}>
      {children}
    </AuthContext.Provider>
  )
}
