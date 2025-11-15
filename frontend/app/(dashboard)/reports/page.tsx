'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useReports } from '@/hooks/useReports';
import { ReportUpload } from '@/components/dashboard/ReportUpload';
import { ReportsList } from '@/components/dashboard/ReportsList';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FileText, Upload } from 'lucide-react';

export default function ReportsPage() {
  const searchParams = useSearchParams();
  const { fetchReports } = useReports();
  const [activeTab, setActiveTab] = useState(
    searchParams.get('upload') === 'true' ? 'upload' : 'list'
  );

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Medical Reports</h1>
        <p className="text-muted-foreground">
          Manage and analyze your medical reports with AI-powered insights
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList>
          <TabsTrigger value="list" className="flex items-center gap-2">
            <FileText className="h-4 w-4" />
            My Reports
          </TabsTrigger>
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            Upload Report
          </TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="space-y-6">
          <ReportsList />
        </TabsContent>

        <TabsContent value="upload" className="space-y-6">
          <ReportUpload />
        </TabsContent>
      </Tabs>
    </div>
  );
}
