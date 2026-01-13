import React, { createContext, useState, useContext, useEffect } from 'react'
import { api } from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored auth data
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    if (storedToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser)
        setToken(storedToken)
        setUser(parsedUser)
        api.setToken(storedToken)
        
        // Verify token is still valid (don't block if backend is down)
        verifyToken(storedToken)
      } catch (error) {
        // If anything fails, just clear and continue
        console.error('Error loading auth data:', error)
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        setToken(null)
        setUser(null)
        setLoading(false)
      }
    } else {
      // No stored auth data, user is not authenticated
      setToken(null)
      setUser(null)
      setLoading(false)
    }
  }, [])

  const verifyToken = async (tokenToVerify) => {
    try {
      // Set token in API client
      api.setToken(tokenToVerify)
      
      // Verify with backend
      const response = await api.getCurrentUser()
      if (response.data && response.data.success) {
        setUser(response.data.data)
        setToken(tokenToVerify)
      } else {
        // Token invalid, clear storage but don't redirect yet
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        setUser(null)
        setToken(null)
      }
    } catch (error) {
      // Backend might be down or token invalid
      // Clear storage but don't force redirect
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      setUser(null)
      setToken(null)
    } finally {
      setLoading(false)
    }
  }

  const login = (userData, authToken) => {
    setUser(userData)
    setToken(authToken)
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
    api.setToken(authToken)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    api.setToken(null)
    // Navigation will be handled by ProtectedRoute component
    window.location.href = '/login'
  }

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user && !!token,
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

