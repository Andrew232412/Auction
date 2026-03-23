# API Endpoints Documentation

Base URL: `http://localhost:8000/api`

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Creates a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `409 Conflict` - Email or username already exists
- `400 Bad Request` - Invalid input data

---

### Login
**POST** `/auth/login`

Authenticates user and returns JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials

---

### Refresh Token
**POST** `/auth/refresh`

Refreshes access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

---

## User Endpoints

### Get User
**GET** `/users/{id}`

Retrieves user information by ID.

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

### List Users
**GET** `/users`

Retrieves paginated list of users.

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `limit` (optional, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "email": "user@example.com",
      "username": "username",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "pages": 3,
  "limit": 20
}
```

---

### Update User
**PUT** `/users/{id}`

Updates user information. Requires authentication.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "password": "newpassword123"
}
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "newemail@example.com",
  "username": "newusername",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Cannot update other user's profile
- `404 Not Found` - User not found
- `409 Conflict` - Email or username already taken

---

### Delete User
**DELETE** `/users/{id}`

Deletes user account. Requires authentication.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Cannot delete other user's account
- `404 Not Found` - User not found

---

## Auction Endpoints

### Create Auction
**POST** `/auctions`

Creates a new auction. Requires authentication.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Vintage Camera",
  "description": "Rare vintage camera in excellent condition",
  "category": "Electronics",
  "starting_price": 100.00,
  "start_date": "2024-01-20T10:00:00Z",
  "end_date": "2024-01-27T10:00:00Z"
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Vintage Camera",
  "description": "Rare vintage camera in excellent condition",
  "category": "Electronics",
  "starting_price": 100.00,
  "current_price": 100.00,
  "start_date": "2024-01-20T10:00:00Z",
  "end_date": "2024-01-27T10:00:00Z",
  "owner_id": "507f1f77bcf86cd799439011",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `400 Bad Request` - Invalid dates or data

---

### Get Auction
**GET** `/auctions/{id}`

Retrieves auction details by ID.

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Vintage Camera",
  "description": "Rare vintage camera in excellent condition",
  "category": "Electronics",
  "starting_price": 100.00,
  "current_price": 150.00,
  "start_date": "2024-01-20T10:00:00Z",
  "end_date": "2024-01-27T10:00:00Z",
  "owner_id": "507f1f77bcf86cd799439011",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Auction not found

---

### List Auctions
**GET** `/auctions`

Retrieves paginated list of auctions with filtering and sorting.

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `limit` (optional, default: 20, max: 100) - Items per page
- `category` (optional) - Filter by category
- `status` (optional) - Filter by status (active, closed, cancelled)
- `sort_by` (optional, default: created_at) - Sort field (created_at, current_price, end_date, title)
- `sort_order` (optional, default: -1) - Sort order (-1 for descending, 1 for ascending)

**Example:** `/auctions?category=Electronics&status=active&sort_by=current_price&page=1&limit=10`

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439012",
      "title": "Vintage Camera",
      "description": "Rare vintage camera in excellent condition",
      "category": "Electronics",
      "starting_price": 100.00,
      "current_price": 150.00,
      "start_date": "2024-01-20T10:00:00Z",
      "end_date": "2024-01-27T10:00:00Z",
      "owner_id": "507f1f77bcf86cd799439011",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "pages": 3,
  "limit": 10
}
```

---

### Update Auction
**PUT** `/auctions/{id}`

Updates auction details. Requires authentication and ownership.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "end_date": "2024-01-28T10:00:00Z"
}
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Updated Title",
  "description": "Updated description",
  "category": "Electronics",
  "starting_price": 100.00,
  "current_price": 150.00,
  "start_date": "2024-01-20T10:00:00Z",
  "end_date": "2024-01-28T10:00:00Z",
  "owner_id": "507f1f77bcf86cd799439011",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not auction owner
- `404 Not Found` - Auction not found
- `400 Bad Request` - Invalid data or cannot update closed auction

---

### Delete Auction
**DELETE** `/auctions/{id}`

Deletes auction. Requires authentication and ownership. Cannot delete auctions with bids.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not auction owner
- `404 Not Found` - Auction not found
- `400 Bad Request` - Cannot delete auction with active bids

---

## Bid Endpoints

### Place Bid
**POST** `/bids/auctions/{auction_id}/bids`

Places a bid on an auction. Requires authentication.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "amount": 160.00
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439013",
  "auction_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "amount": 160.00,
  "timestamp": "2024-01-16T15:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Cannot bid on own auction
- `404 Not Found` - Auction not found
- `400 Bad Request` - Bid amount too low or auction not active

---

### Get Auction Bids
**GET** `/bids/auctions/{auction_id}/bids`

Retrieves paginated bid history for an auction.

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `limit` (optional, default: 50, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439013",
      "auction_id": "507f1f77bcf86cd799439012",
      "user_id": "507f1f77bcf86cd799439011",
      "amount": 160.00,
      "timestamp": "2024-01-16T15:30:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "pages": 1,
  "limit": 50
}
```

**Error Responses:**
- `404 Not Found` - Auction not found

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "ErrorType",
  "message": "Human readable error message",
  "details": {}
}
```

## HTTP Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate email)
- `500 Internal Server Error` - Server error

## Authentication

Most endpoints require authentication using JWT tokens. Include the access token in the Authorization header:

```
Authorization: Bearer {access_token}
```

Tokens expire after 15 minutes. Use the refresh token endpoint to get a new access token.
