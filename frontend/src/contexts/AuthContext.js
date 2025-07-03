import { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { userAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if the user is already logged in (token exists in localStorage)
  useEffect(() => {
    const checkLoggedIn = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          // Check token expiration
          const decoded = jwtDecode(token);
          const currentTime = Date.now() / 1000;
          
          if (decoded.exp < currentTime) {
            // Token expired, clear localStorage
            logout();
            setLoading(false);
            return;
          }
          
          // Token is valid, fetch current user data
          const response = await userAPI.getCurrentUser();
          setCurrentUser(response.data);
        } catch (err) {
          console.error('Failed to fetch user data:', err);
          logout();
        }
      }
      
      setLoading(false);
    };

    checkLoggedIn();
  }, []);

  // Login user and save token to localStorage
  const login = async (token) => {
    localStorage.setItem('token', token);
    
    try {
      // Fetch current user data
      const response = await userAPI.getCurrentUser();
      setCurrentUser(response.data);
      setError(null);
      return response.data;
    } catch (err) {
      setError('Failed to fetch user data');
      logout();
      throw err;
    }
  };

  // Logout user and clear localStorage
  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
  };

  // Update user profile
  const updateProfile = async (userData) => {
    try {
      const response = await userAPI.updateProfile(userData);
      setCurrentUser(response.data);
      return response.data;
    } catch (err) {
      setError('Failed to update profile');
      throw err;
    }
  };

  const value = {
    currentUser,
    loading,
    error,
    login,
    logout,
    updateProfile,
    isAuthenticated: !!currentUser,
    isAdmin: currentUser?.is_admin || false,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
