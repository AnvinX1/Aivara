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
          // Don't redirect if we're already on a login page or if it's a login/register endpoint
          if (typeof window !== 'undefined') {
            const currentPath = window.location.pathname;
            const isLoginPage = currentPath === '/login' || currentPath === '/doctor/login';
            const isRegisterPage = currentPath === '/register' || currentPath === '/doctor/register';
            const requestUrl = error.config?.url || '';
            const isAuthEndpoint = requestUrl.includes('/token') || 
                                 requestUrl.includes('/register') || 
                                 requestUrl.includes('/token_doctor') ||
                                 requestUrl.includes('/register_doctor');
            
            // Only redirect if not already on login/register page and not an auth endpoint
            if (!isLoginPage && !isRegisterPage && !isAuthEndpoint) {
              const userStr = localStorage.getItem('user');
              let isDoctor = false;
              
              try {
                if (userStr) {
                  const user = JSON.parse(userStr);
                  isDoctor = user?.role === 'doctor';
                } else {
                  // If no user data but on doctor route, assume doctor
                  isDoctor = currentPath?.startsWith('/doctor') || false;
                }
              } catch {
                // If parsing fails, check current path
                isDoctor = currentPath?.startsWith('/doctor') || false;
              }
              
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              
              // Redirect to appropriate login page based on user role or current path
              window.location.href = isDoctor ? '/doctor/login' : '/login';
            }
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

  // Hospital endpoints
  async getHospitals(city?: string, state?: string) {
    const params: any = {};
    if (city) params.city = city;
    if (state) params.state = state;
    const response = await this.client.get('/hospitals/', { params });
    return response.data;
  }

  async getHospital(hospitalId: number) {
    const response = await this.client.get(`/hospitals/${hospitalId}`);
    return response.data;
  }

  async getHospitalDoctors(hospitalId: number, specialization?: string) {
    const params: any = {};
    if (specialization) params.specialization = specialization;
    const response = await this.client.get(`/hospitals/${hospitalId}/doctors`, { params });
    return response.data;
  }

  // Report sharing endpoints
  async shareReportToDoctor(reportId: number, doctorId: number, message?: string) {
    const response = await this.client.post(`/reports/${reportId}/share`, {
      doctor_id: doctorId,
      patient_message: message,
    });
    return response.data;
  }

  async getSharedReports() {
    const response = await this.client.get('/reports/shared');
    return response.data;
  }

  async cancelSharing(reportId: number, sharingId: number) {
    const response = await this.client.put(`/reports/${reportId}/cancel-sharing/${sharingId}`);
    return response.data;
  }

  // Doctor endpoints (for doctor portal)
  async doctorLogin(email: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const response = await this.client.post('/doctor/token_doctor', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  async doctorRegister(
    email: string,
    password: string,
    fullName: string,
    specialization?: string,
    hospitalId?: number,
    phone?: string,
    registrationNumber?: string
  ) {
    const response = await this.client.post('/doctor/register_doctor', {
      email,
      password,
      full_name: fullName,
      specialization,
      hospital_id: hospitalId,
      phone,
      registration_number: registrationNumber,
    });
    return response.data;
  }

  async getDoctorPendingReports(statusFilter?: string) {
    const params: any = {};
    if (statusFilter) params.status_filter = statusFilter;
    const response = await this.client.get('/doctor/reports/pending', { params });
    return response.data;
  }

  async getDoctorReport(reportId: number) {
    const response = await this.client.get(`/doctor/reports/${reportId}`);
    return response.data;
  }

  async reviewReport(reportId: number, aiApprovalStatus: string, doctorNotes: string, reviewStatus: string) {
    const response = await this.client.post(`/doctor/reports/${reportId}/review`, {
      ai_approval_status: aiApprovalStatus,
      doctor_notes: doctorNotes,
      review_status: reviewStatus,
    });
    return response.data;
  }

  async getDoctorReviewedReports(skip = 0, limit = 100) {
    const response = await this.client.get('/doctor/reports/reviewed', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getDoctorProfile() {
    const response = await this.client.get('/doctor/profile');
    return response.data;
  }

  // Forecasting endpoints
  async generateForecast(reportId: number, forecastType = 'health_trends') {
    const response = await this.client.post(`/forecasting/${reportId}/predict`, null, {
      params: { forecast_type: forecastType },
    });
    return response.data;
  }

  async getForecast(reportId: number, forecastType?: string) {
    const params: any = {};
    if (forecastType) params.forecast_type = forecastType;
    const response = await this.client.get(`/forecasting/${reportId}`, { params });
    return response.data;
  }

  async getPatientForecastTrends(patientId: number) {
    const response = await this.client.get(`/forecasting/patient/${patientId}/trends`);
    return response.data;
  }
}

export const api = new ApiClient();
export default api;
