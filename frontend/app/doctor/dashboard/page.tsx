"use client";

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import api from '@/lib/api';
import { FileText, Clock, CheckCircle, User, Loader2, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

interface PendingReport {
  report: {
    id: number;
    report_name: string;
    upload_timestamp: string;
    hemoglobin: number | null;
    wbc: number | null;
    platelets: number | null;
    rbc: number | null;
    analysis_result_json: string | null;
    review_status: string;
    ai_approval_status: string;
  };
  patient: {
    id: number;
    full_name: string | null;
    email: string;
  };
  sharing: {
    id: number;
    status: string;
    patient_message: string | null;
    sent_at: string;
    created_at: string;
  };
}

export default function DoctorDashboardPage() {
  const [pendingReports, setPendingReports] = useState<PendingReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    pending: 0,
    reviewedToday: 0,
    total: 0,
  });

  useEffect(() => {
    // Only fetch if we have a token (to prevent 401 errors)
    if (typeof window !== 'undefined' && localStorage.getItem('token')) {
      fetchPendingReports();
    }
  }, []);

  const fetchPendingReports = async () => {
    try {
      setLoading(true);
      
      // Verify we have a token before making the request
      if (typeof window === 'undefined' || !localStorage.getItem('token')) {
        console.error('No token available');
        return;
      }
      
      const data = await api.getDoctorPendingReports();
      setPendingReports(data);
      setStats({
        pending: data.length,
        reviewedToday: 0, // TODO: Calculate from reviewed reports
        total: data.length,
      });
    } catch (error: any) {
      // Don't show error if it's a 401 (will be handled by interceptor)
      if (error.response?.status !== 401) {
        toast.error('Failed to load reports', {
          description: error.response?.data?.detail || 'Please try again',
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Doctor Dashboard</h1>
        <p className="text-muted-foreground">Manage and review patient reports</p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Reviews</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pending}</div>
            <p className="text-xs text-muted-foreground">Reports awaiting review</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Reviewed Today</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.reviewedToday}</div>
            <p className="text-xs text-muted-foreground">Reports reviewed today</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reports</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-muted-foreground">All reports</p>
          </CardContent>
        </Card>
      </div>

      {/* Pending Reports */}
      <Card>
        <CardHeader>
          <CardTitle>Pending Reports</CardTitle>
          <CardDescription>Reports that need your review</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin" />
            </div>
          ) : pendingReports.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No pending reports at the moment
            </div>
          ) : (
            <div className="space-y-4">
              {pendingReports.map((item) => (
                <Card key={item.sharing.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <FileText className="h-5 w-5 text-primary" />
                          <h3 className="text-lg font-semibold">{item.report.report_name}</h3>
                          <Badge variant="outline">{item.sharing.status}</Badge>
                        </div>
                        <div className="space-y-2 text-sm text-muted-foreground">
                          <div className="flex items-center gap-2">
                            <User className="h-4 w-4" />
                            <span>
                              Patient: {item.patient.full_name || item.patient.email}
                            </span>
                          </div>
                          <div>
                            Sent: {format(new Date(item.sharing.sent_at), 'PPpp')}
                          </div>
                          {item.sharing.patient_message && (
                            <div className="mt-2 p-2 bg-muted rounded-md">
                              <p className="text-xs font-medium mb-1">Patient Message:</p>
                              <p className="text-sm">{item.sharing.patient_message}</p>
                            </div>
                          )}
                        </div>
                      </div>
                      <Link href={`/doctor/reports/${item.report.id}`}>
                        <Button>
                          Review
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

