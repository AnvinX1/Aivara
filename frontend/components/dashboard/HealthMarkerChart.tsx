'use client';

import { useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity } from 'lucide-react';
import { gsap } from 'gsap';
import type { Report } from '@/hooks/useReports';

interface HealthMarkerChartProps {
  report: Report;
}

interface ChartData {
  name: string;
  value: number | null;
  normalMin: number;
  normalMax: number;
  status: 'normal' | 'low' | 'high' | null;
}

export function HealthMarkerChart({ report }: HealthMarkerChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chartRef.current) {
      gsap.fromTo(
        chartRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }
      );
    }
  }, []);

  const chartData: ChartData[] = [
    {
      name: 'Hemoglobin',
      value: report.hemoglobin,
      normalMin: 13.5,
      normalMax: 17.5,
      status: report.hemoglobin
        ? report.hemoglobin < 13.5
          ? 'low'
          : report.hemoglobin > 17.5
          ? 'high'
          : 'normal'
        : null,
    },
    {
      name: 'WBC',
      value: report.wbc,
      normalMin: 4.5,
      normalMax: 11.0,
      status: report.wbc
        ? report.wbc < 4.5
          ? 'low'
          : report.wbc > 11.0
          ? 'high'
          : 'normal'
        : null,
    },
    {
      name: 'Platelets',
      value: report.platelets,
      normalMin: 150,
      normalMax: 450,
      status: report.platelets
        ? report.platelets < 150
          ? 'low'
          : report.platelets > 450
          ? 'high'
          : 'normal'
        : null,
    },
    {
      name: 'RBC',
      value: report.rbc,
      normalMin: 4.32,
      normalMax: 5.72,
      status: report.rbc
        ? report.rbc < 4.32
          ? 'low'
          : report.rbc > 5.72
          ? 'high'
          : 'normal'
        : null,
    },
  ].filter((item) => item.value !== null) as ChartData[];

  const formatDataForChart = () => {
    return chartData.map((item) => ({
      name: item.name,
      value: item.value || 0,
      'Normal Min': item.normalMin,
      'Normal Max': item.normalMax,
    }));
  };

  const getBarColor = (status: 'normal' | 'low' | 'high' | null) => {
    switch (status) {
      case 'normal':
        return '#22c55e'; // green-500
      case 'low':
        return '#f59e0b'; // amber-500
      case 'high':
        return '#ef4444'; // red-500
      default:
        return '#6b7280'; // gray-500
    }
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const marker = chartData.find((item) => item.name === data.name);
      return (
        <div className="bg-background border rounded-lg p-3 shadow-lg">
          <p className="font-semibold mb-2">{data.name}</p>
          <p className="text-sm">
            <span className="text-muted-foreground">Value: </span>
            <span className="font-medium">{data.value}</span>
          </p>
          <p className="text-sm">
            <span className="text-muted-foreground">Normal Range: </span>
            <span className="font-medium">
              {data['Normal Min']} - {data['Normal Max']}
            </span>
          </p>
          {marker?.status && (
            <p className="text-sm mt-1">
              <span className="text-muted-foreground">Status: </span>
              <span
                className={`font-medium ${
                  marker.status === 'normal'
                    ? 'text-green-500'
                    : marker.status === 'low'
                    ? 'text-amber-500'
                    : 'text-red-500'
                }`}
              >
                {marker.status === 'normal' ? 'Normal' : marker.status === 'low' ? 'Below Normal' : 'Above Normal'}
              </span>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  if (chartData.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Health Markers Visualization
          </CardTitle>
          <CardDescription>No health marker data available for visualization</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div ref={chartRef}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Health Markers Visualization
          </CardTitle>
          <CardDescription>Current health marker values compared to normal ranges</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-4 flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-green-500"></div>
              <span className="text-sm">Normal Range</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-amber-500"></div>
              <span className="text-sm">Below Normal</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-red-500"></div>
              <span className="text-sm">Above Normal</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={formatDataForChart()} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="name" className="text-xs" />
              <YAxis className="text-xs" />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <ReferenceLine y={0} stroke="#888" />
              {chartData.map((item, index) => (
                <Bar
                  key={item.name}
                  dataKey="value"
                  fill={getBarColor(item.status)}
                  radius={[8, 8, 0, 0]}
                  name={item.name}
                  animationDuration={1000}
                  animationBegin={index * 100}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}

