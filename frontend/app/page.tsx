'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Activity } from 'lucide-react';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      const userStr = localStorage.getItem('user');
      
      if (token && userStr) {
        try {
          const user = JSON.parse(userStr);
          // Check if user is a doctor
          if (user.role === 'doctor') {
            router.push('/doctor/dashboard');
          } else {
            router.push('/dashboard');
          }
        } catch {
          router.push('/login');
        }
      } else {
        router.push('/login');
      }
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Activity className="w-8 h-8 animate-pulse text-primary" />
    </div>
  );
}