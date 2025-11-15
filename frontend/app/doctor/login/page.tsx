"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import api from '@/lib/api';
import { Loader2, User, Activity } from 'lucide-react';
import Link from 'next/link';

export default function DoctorLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.doctorLogin(email, password);
      
      if (!response || !response.access_token) {
        throw new Error('Invalid response from server');
      }
      
      if (typeof window !== 'undefined') {
        // Store token and user with doctor role FIRST
        localStorage.setItem('token', response.access_token);
        const userData = { 
          role: 'doctor', 
          email: email,
          access_token: response.access_token 
        };
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Verify storage was successful
        const storedToken = localStorage.getItem('token');
        const storedUserStr = localStorage.getItem('user');
        
        if (!storedToken || !storedUserStr) {
          throw new Error('Failed to store authentication data');
        }
        
        // Parse to verify it's valid JSON
        try {
          const storedUser = JSON.parse(storedUserStr);
          if (storedUser.role !== 'doctor') {
            throw new Error('User role not set correctly');
          }
        } catch (e) {
          throw new Error('Failed to verify stored user data');
        }
        
        // Verify one more time before redirecting
        const finalTokenCheck = localStorage.getItem('token');
        const finalUserCheck = localStorage.getItem('user');
        
        if (!finalTokenCheck || !finalUserCheck) {
          throw new Error('Authentication data lost before redirect');
        }
        
        // Show success message
        toast.success('Login successful', {
          description: 'Welcome back, Doctor! Redirecting...',
        });
        
        // Use window.location.replace for immediate redirect (prevents back button and Next.js router issues)
        // Immediate redirect without delay to prevent any intermediate checks
        window.location.replace('/doctor/dashboard');
        return; // Exit early to prevent error handling
      }
    } catch (error: any) {
      console.error('Doctor login error:', error);
      toast.error('Login failed', {
        description: error.response?.data?.detail || error.message || 'Please check your credentials',
      });
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/5 via-background to-primary/5 p-4">
      <div className="absolute top-4 left-4 flex items-center gap-2">
        <Activity className="h-6 w-6 text-primary" />
        <span className="text-xl font-bold">Aivara Healthcare</span>
      </div>
      <Card className="w-full max-w-md shadow-xl">
        <CardHeader className="space-y-1 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
            <User className="h-8 w-8 text-primary" />
          </div>
          <CardTitle className="text-2xl font-bold">Doctor Portal</CardTitle>
            <CardDescription>Sign in to your doctor account</CardDescription>
            <div className="mt-2 text-xs text-muted-foreground bg-muted p-2 rounded">
              <p className="font-semibold mb-1">Test Credentials:</p>
              <p>Email: ravi.kumar@kmchhospitals.com</p>
              <p>Password: Doctor@123</p>
            </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="doctor@hospital.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </form>
          <div className="mt-4 space-y-2 text-center text-sm text-muted-foreground">
            <div>
              Don't have an account?{' '}
              <Link href="/doctor/register" className="underline hover:text-primary font-medium">
                Register as Doctor
              </Link>
            </div>
            <div>
              <Link href="/login" className="underline hover:text-primary">
                Patient login instead?
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

