'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { Toaster } from '@/components/ui/sonner';
import { Activity } from 'lucide-react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      const userStr = localStorage.getItem('user');
      
      if (!token) {
        router.push('/login');
        return;
      }
      
      // Check if user is a doctor trying to access patient dashboard
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          if (user.role === 'doctor') {
            // Doctor accessing patient dashboard - redirect to doctor dashboard
            router.push('/doctor/dashboard');
          }
        } catch {
          // Invalid user data, redirect to login
          router.push('/login');
        }
      }
    }
  }, [router, pathname]);

  if (typeof window !== 'undefined' && !localStorage.getItem('token')) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Activity className="w-8 h-8 animate-pulse text-primary" />
      </div>
    );
  }

  return (
    <>
      <Header />
      <Sidebar />
      <main className="flex-1 min-h-screen pt-16 md:pl-64">
        {children}
      </main>
      <Toaster />
    </>
  );
}
