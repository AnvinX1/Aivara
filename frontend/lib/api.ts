import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add token
    this.client.interceptors.request.use(
      (config) => {
        if (typeof window !== 'undefined') {
          const token = localStorage.getItem('token');
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(email: string, password: string, fullName: string) {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  }

  async login(email: string, password: string) {
    // OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const response = await this.client.post('/auth/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  // Report endpoints
  async getReports() {
    const response = await this.client.get('/reports/');
    return response.data;
  }

  async getReport(reportId: number, includeExtractedText = false) {
    const response = await this.client.get(`/reports/${reportId}`, {
      params: { include_extracted_text: includeExtractedText },
    });
    return response.data;
  }

  async uploadReport(reportName: string, file: File) {
    const formData = new FormData();
    formData.append('report_name', reportName);
    formData.append('file', file);

    const response = await this.client.post('/reports/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async reanalyzeReport(reportId: number) {
    const response = await this.client.post(`/ai/analyze/${reportId}`);
    return response.data;
  }

  async getMedicineSuggestions(reportId: number) {
    const response = await this.client.get(`/reports/${reportId}/medicine-suggestions`);
    return response.data;
  }

  async getWomenHealthSuggestions(reportId: number) {
    const response = await this.client.get(`/reports/${reportId}/women-health`);
    return response.data;
  }
}

export const api = new ApiClient();
export default api;
