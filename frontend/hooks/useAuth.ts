'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { setAuthToken, removeAuthToken, setUser, getUser, isAuthenticated as checkAuth } from '@/lib/auth';
import type { User } from '@/lib/auth';

export function useAuth() {
  const router = useRouter();
  const [user, setUserState] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedUser = getUser();
      setUserState(storedUser);
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const response = await api.login(email, password);
      setAuthToken(response.access_token);
      
      // Get user info from token or fetch it
      // For now, we'll store email from login
      const userData: User = {
        id: 0, // Will be populated from API if available
        email,
        full_name: email, // Will be populated from API if available
      };
      setUser(userData);
      setUserState(userData);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed',
      };
    }
  }, []);

  const register = useCallback(async (email: string, password: string, fullName: string) => {
    try {
      const response = await api.register(email, password, fullName);
      setUser(response);
      setUserState(response);
      
      // Auto-login after registration
      const loginResponse = await api.login(email, password);
      setAuthToken(loginResponse.access_token);
      
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Registration failed',
      };
    }
  }, []);

  const logout = useCallback(() => {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('user');
      const isDoctor = userStr ? (JSON.parse(userStr)?.role === 'doctor') : false;
      
      removeAuthToken();
      setUserState(null);
      
      // Redirect to appropriate login page based on user role
      router.push(isDoctor ? '/doctor/login' : '/login');
    }
  }, [router]);

  return {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: checkAuth(),
  };
}
