'use client';

import { useState, useCallback } from 'react';
import { api } from '@/lib/api';

export interface Report {
  id: number;
  report_name: string;
  upload_timestamp: string;
  file_path: string;
  hemoglobin: number | null;
  wbc: number | null;
  platelets: number | null;
  rbc: number | null;
  analysis_results?: any;
  extracted_text?: string;
}

export function useReports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getReports();
      setReports(data);
      return { success: true, data };
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch reports';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchReport = useCallback(async (reportId: number, includeText = false) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getReport(reportId, includeText);
      return { success: true, data };
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch report';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  }, []);

  const uploadReport = useCallback(async (reportName: string, file: File) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.uploadReport(reportName, file);
      // Refresh reports list
      await fetchReports();
      return { success: true, data };
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to upload report';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  }, [fetchReports]);

  const reanalyzeReport = useCallback(async (reportId: number) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.reanalyzeReport(reportId);
      return { success: true, data };
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to reanalyze report';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    reports,
    loading,
    error,
    fetchReports,
    fetchReport,
    uploadReport,
    reanalyzeReport,
  };
}
