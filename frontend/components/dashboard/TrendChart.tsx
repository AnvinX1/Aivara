'use client';

import { useEffect, useRef, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';
import { gsap } from 'gsap';
import { format } from 'date-fns';
import type { Report } from '@/hooks/useReports';

interface TrendChartProps {
  currentReport: Report;
  allReports: Report[];
}

export function TrendChart({ currentReport, allReports }: TrendChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chartRef.current) {
      gsap.fromTo(
        chartRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', delay: 0.2 }
      );
    }
  }, []);

  // Combine all reports including current one, sorted by date
  const reports = useMemo(() => {
    const combined = [...allReports, currentReport].filter((r) => r.id !== currentReport.id || !allReports.find((ar) => ar.id === currentReport.id));
    return combined
      .sort((a, b) => new Date(a.upload_timestamp).getTime() - new Date(b.upload_timestamp).getTime())
      .filter((r) => r.hemoglobin !== null || r.wbc !== null || r.platelets !== null || r.rbc !== null);
  }, [allReports, currentReport]);

  const chartData = useMemo(() => {
    return reports.map((report) => ({
      date: format(new Date(report.upload_timestamp), 'MMM dd'),
      fullDate: format(new Date(report.upload_timestamp), 'yyyy-MM-dd'),
      Hemoglobin: report.hemoglobin,
      WBC: report.wbc,
      Platelets: report.platelets ? report.platelets / 10 : null, // Scale down for better visualization
      RBC: report.rbc,
    }));
  }, [reports]);

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-background border rounded-lg p-3 shadow-lg">
          <p className="font-semibold mb-2">{data.fullDate}</p>
          {payload.map((entry: any, index: number) => {
            if (entry.value === null || entry.value === undefined) return null;
            return (
              <p key={index} className="text-sm" style={{ color: entry.color }}>
                <span className="font-medium">{entry.name}: </span>
                <span>{entry.name === 'Platelets' ? (entry.value * 10).toFixed(0) : entry.value.toFixed(2)}</span>
              </p>
            );
          })}
        </div>
      );
    }
    return null;
  };

  if (chartData.length < 2) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Historical Trends
          </CardTitle>
          <CardDescription>Track your health markers over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="py-12 text-center text-muted-foreground">
            <p>Upload at least 2 reports to view historical trends</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div ref={chartRef}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Historical Trends
          </CardTitle>
          <CardDescription>Track your health markers over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="date" className="text-xs" />
              <YAxis className="text-xs" />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                type="monotone"
                dataKey="Hemoglobin"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                animationDuration={1000}
                name="Hemoglobin (g/dL)"
              />
              <Line
                type="monotone"
                dataKey="WBC"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                animationDuration={1200}
                name="WBC (x10³/μL)"
              />
              <Line
                type="monotone"
                dataKey="Platelets"
                stroke="#f59e0b"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                animationDuration={1400}
                name="Platelets (x10³/μL) [×10]"
              />
              <Line
                type="monotone"
                dataKey="RBC"
                stroke="#ef4444"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                animationDuration={1600}
                name="RBC (x10⁶/μL)"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}

