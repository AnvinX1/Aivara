'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DoctorDashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      const userStr = localStorage.getItem('user');
      
      if (!token) {
        window.location.replace('/doctor/login');
        return;
      }
      
      // Verify user is a doctor
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          if (user.role !== 'doctor') {
            // Not a doctor, redirect to patient dashboard
            window.location.replace('/dashboard');
            return;
          }
          // Valid doctor - allow access, don't redirect
        } catch {
          // Invalid user data, redirect to doctor login
          window.location.replace('/doctor/login');
          return;
        }
      } else {
        // No user data, redirect to doctor login
        window.location.replace('/doctor/login');
        return;
      }
    }
  }, []);

  if (typeof window !== 'undefined' && !localStorage.getItem('token')) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return <>{children}</>;
}

