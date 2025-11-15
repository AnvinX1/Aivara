'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Calendar, User, Activity } from 'lucide-react';
import { format } from 'date-fns';
import type { Report } from '@/hooks/useReports';

interface ReportDetailsProps {
  report: Report;
}

export function ReportDetails({ report }: ReportDetailsProps) {
  const getMarkerStatus = (value: number | null, normalMin: number, normalMax: number) => {
    if (value === null) return null;
    if (value < normalMin) return 'low';
    if (value > normalMax) return 'high';
    return 'normal';
  };

  const markers = [
    {
      name: 'Hemoglobin',
      value: report.hemoglobin,
      unit: 'g/dL',
      normalRange: { min: 13.5, max: 17.5 },
      status: getMarkerStatus(report.hemoglobin, 13.5, 17.5),
    },
    {
      name: 'WBC (White Blood Cells)',
      value: report.wbc,
      unit: 'x10³/μL',
      normalRange: { min: 4.5, max: 11.0 },
      status: getMarkerStatus(report.wbc, 4.5, 11.0),
    },
    {
      name: 'Platelets',
      value: report.platelets,
      unit: 'x10³/μL',
      normalRange: { min: 150, max: 450 },
      status: getMarkerStatus(report.platelets, 150, 450),
    },
    {
      name: 'RBC (Red Blood Cells)',
      value: report.rbc,
      unit: 'x10⁶/μL',
      normalRange: { min: 4.32, max: 5.72 },
      status: getMarkerStatus(report.rbc, 4.32, 5.72),
    },
  ];

  return (
    <div className="space-y-6">
      <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300">
        <CardHeader className="bg-gradient-to-r from-primary/5 to-transparent border-b">
          <CardTitle className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-primary/10">
              <FileText className="h-5 w-5 text-primary" />
            </div>
            Report Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Report Name</p>
              <p className="text-lg font-semibold">{report.report_name}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Report ID</p>
              <p className="text-lg font-semibold">#{report.id}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                Upload Date
              </p>
              <p className="text-lg">
                {format(new Date(report.upload_timestamp), 'PPpp')}
              </p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">File Path</p>
              <p className="text-sm text-muted-foreground break-all">{report.file_path}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300">
        <CardHeader className="bg-gradient-to-r from-green-50 to-transparent dark:from-green-950/20 border-b">
          <CardTitle className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-green-500/10">
              <Activity className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            Health Markers
          </CardTitle>
          <CardDescription>Extracted health marker values from the report</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid gap-4 md:grid-cols-2">
            {markers.map((marker) => (
              <div
                key={marker.name}
                className="p-5 border rounded-xl space-y-3 bg-gradient-to-br from-card to-muted/20 hover:shadow-md transition-all duration-200 hover:border-primary/30"
              >
                <div className="flex items-center justify-between">
                  <p className="font-medium">{marker.name}</p>
                  {marker.status && (
                    <Badge
                      variant={
                        marker.status === 'normal'
                          ? 'default'
                          : marker.status === 'low'
                          ? 'secondary'
                          : 'destructive'
                      }
                    >
                      {marker.status === 'normal' ? 'Normal' : marker.status === 'low' ? 'Low' : 'High'}
                    </Badge>
                  )}
                </div>
                <div className="flex items-baseline gap-2">
                  {marker.value !== null ? (
                    <>
                      <span className="text-2xl font-bold">{marker.value}</span>
                      <span className="text-sm text-muted-foreground">{marker.unit}</span>
                    </>
                  ) : (
                    <span className="text-muted-foreground">N/A</span>
                  )}
                </div>
                {marker.value !== null && (
                  <p className="text-xs text-muted-foreground">
                    Normal range: {marker.normalRange.min} - {marker.normalRange.max} {marker.unit}
                  </p>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {report.extracted_text && (
        <Card>
          <CardHeader>
            <CardTitle>Extracted Text</CardTitle>
            <CardDescription>OCR extracted text from the report</CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="p-4 bg-muted rounded-lg text-sm whitespace-pre-wrap max-h-96 overflow-y-auto">
              {report.extracted_text}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
