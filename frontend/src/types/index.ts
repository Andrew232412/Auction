export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserUpdate {
  email?: string;
  username?: string;
  password?: string;
}

export enum AuctionStatus {
  ACTIVE = 'active',
  CLOSED = 'closed',
  CANCELLED = 'cancelled'
}

export interface Auction {
  id: string;
  title: string;
  description: string;
  category: string;
  starting_price: number;
  current_price: number;
  start_date: string;
  end_date: string;
  owner_id: string;
  status: AuctionStatus;
  created_at: string;
}

export interface AuctionCreate {
  title: string;
  description: string;
  category: string;
  starting_price: number;
  start_date: string;
  end_date: string;
}

export interface AuctionUpdate {
  title?: string;
  description?: string;
  category?: string;
  starting_price?: number;
  end_date?: string;
  status?: AuctionStatus;
}

export interface Bid {
  id: string;
  auction_id: string;
  user_id: string;
  amount: number;
  timestamp: string;
}

export interface BidCreate {
  amount: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
  limit: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiError {
  error: string;
  message: string;
  details: Record<string, unknown>;
}
