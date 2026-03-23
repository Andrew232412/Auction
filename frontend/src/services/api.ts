import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  UserCreate,
  UserUpdate,
  Auction,
  AuctionCreate,
  AuctionUpdate,
  Bid,
  BidCreate,
  PaginatedResponse,
  LoginRequest,
  TokenResponse
} from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post<TokenResponse>(`${API_URL}/api/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: UserCreate) => api.post<User>('/auth/register', data),
  login: (data: LoginRequest) => api.post<TokenResponse>('/auth/login', data),
  refresh: (refreshToken: string) => 
    api.post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken }),
};

export const usersAPI = {
  getUser: (id: string) => api.get<User>(`/users/${id}`),
  getUsers: (params?: Record<string, any>) => 
    api.get<PaginatedResponse<User>>('/users', { params }),
  updateUser: (id: string, data: UserUpdate) => api.put<User>(`/users/${id}`, data),
  deleteUser: (id: string) => api.delete(`/users/${id}`),
};

export const auctionsAPI = {
  createAuction: (data: AuctionCreate) => api.post<Auction>('/auctions', data),
  getAuction: (id: string) => api.get<Auction>(`/auctions/${id}`),
  getAuctions: (params?: Record<string, any>) => 
    api.get<PaginatedResponse<Auction>>('/auctions', { params }),
  updateAuction: (id: string, data: AuctionUpdate) => 
    api.put<Auction>(`/auctions/${id}`, data),
  deleteAuction: (id: string) => api.delete(`/auctions/${id}`),
};

export const bidsAPI = {
  placeBid: (auctionId: string, data: BidCreate) => 
    api.post<Bid>(`/bids/auctions/${auctionId}/bids`, data),
  getAuctionBids: (auctionId: string, params?: Record<string, any>) => 
    api.get<PaginatedResponse<Bid>>(`/bids/auctions/${auctionId}/bids`, { params }),
};

export default api;
