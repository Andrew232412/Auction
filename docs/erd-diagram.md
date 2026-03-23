# Database Schema (ERD)

## MongoDB Collections

### Users Collection

```
users
├── _id: ObjectId (Primary Key)
├── email: String (Unique, Indexed)
├── username: String (Unique, Indexed)
├── password_hash: String
├── created_at: DateTime
└── updated_at: DateTime
```

**Indexes:**
- `email` (unique)
- `username` (unique)

**Validation:**
- Email must be valid format
- Username and password are required
- Passwords are hashed with bcrypt

---

### Auctions Collection

```
auctions
├── _id: ObjectId (Primary Key)
├── title: String
├── description: String
├── category: String (Indexed)
├── starting_price: Float (> 0)
├── current_price: Float (> 0)
├── start_date: DateTime
├── end_date: DateTime
├── owner_id: String (Foreign Key → users._id, Indexed)
├── status: Enum (active, closed, cancelled) (Indexed)
└── created_at: DateTime (Indexed)
```

**Indexes:**
- `owner_id`
- `category`
- `status`
- `end_date`
- `created_at` (descending)

**Validation:**
- Prices must be positive
- end_date must be after start_date
- Status must be one of: active, closed, cancelled

---

### Bids Collection

```
bids
├── _id: ObjectId (Primary Key)
├── auction_id: String (Foreign Key → auctions._id, Indexed)
├── user_id: String (Foreign Key → users._id, Indexed)
├── amount: Float (> 0)
└── timestamp: DateTime (Indexed)
```

**Indexes:**
- `auction_id`
- `user_id`
- `(auction_id, amount)` (compound, descending on amount)
- `timestamp` (descending)

**Validation:**
- Amount must be positive
- Amount must be higher than current auction price

---

## Entity Relationships

```
┌─────────────────┐
│     Users       │
│                 │
│ _id (PK)        │
│ email (unique)  │
│ username        │
│ password_hash   │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1
         │
         │ owns
         │
         │ N
         │
┌────────▼────────┐
│   Auctions      │
│                 │
│ _id (PK)        │
│ title           │
│ description     │
│ category        │
│ starting_price  │
│ current_price   │
│ start_date      │
│ end_date        │
│ owner_id (FK)   │◄──────────┐
│ status          │           │
│ created_at      │           │
└────────┬────────┘           │
         │                    │
         │ 1                  │
         │                    │
         │ has                │
         │                    │
         │ N                  │
         │                    │
┌────────▼────────┐           │
│      Bids       │           │
│                 │           │
│ _id (PK)        │           │
│ auction_id (FK) │───────────┘
│ user_id (FK)    │───────────┐
│ amount          │           │
│ timestamp       │           │
└─────────────────┘           │
                              │
                              │
                              │
         ┌────────────────────┘
         │
         │ N
         │
         │ places
         │
         │ 1
         │
┌────────▼────────┐
│     Users       │
│                 │
│ (same as above) │
│                 │
└─────────────────┘
```

## Relationships Description

### User → Auctions (One-to-Many)
- One user can create multiple auctions
- Each auction belongs to one user (owner)
- Relationship: `auctions.owner_id` references `users._id`

### Auction → Bids (One-to-Many)
- One auction can have multiple bids
- Each bid belongs to one auction
- Relationship: `bids.auction_id` references `auctions._id`

### User → Bids (One-to-Many)
- One user can place multiple bids
- Each bid is placed by one user
- Relationship: `bids.user_id` references `users._id`

## Data Integrity Rules

### Business Rules

1. **User Registration**
   - Email must be unique
   - Username must be unique
   - Password must be hashed before storage

2. **Auction Creation**
   - Start date cannot be in the past
   - End date must be after start date
   - Starting price must be positive
   - Current price initialized to starting price

3. **Bid Placement**
   - User cannot bid on their own auction
   - Bid amount must be higher than current price
   - Cannot bid on inactive/closed auctions
   - Placing a bid updates auction's current_price

4. **Auction Status**
   - Active: Auction is accepting bids
   - Closed: Auction has ended (automatically or manually)
   - Cancelled: Auction was cancelled by owner

### Referential Integrity

While MongoDB doesn't enforce foreign key constraints, the application layer ensures:
- Auctions reference valid user IDs (owners)
- Bids reference valid auction IDs and user IDs
- Deleting a user should handle their auctions and bids
- Deleting an auction with bids is prevented

## Query Patterns

### Common Queries

1. **Find active auctions by category**
```javascript
db.auctions.find({ 
  category: "Electronics", 
  status: "active" 
}).sort({ created_at: -1 })
```

2. **Find user's auctions**
```javascript
db.auctions.find({ owner_id: "user_id" })
```

3. **Find auction bids (highest first)**
```javascript
db.bids.find({ auction_id: "auction_id" })
  .sort({ amount: -1 })
```

4. **Find highest bid for auction**
```javascript
db.bids.findOne({ auction_id: "auction_id" })
  .sort({ amount: -1 })
```

5. **Count total auctions by status**
```javascript
db.auctions.countDocuments({ status: "active" })
```

## Performance Considerations

### Index Strategy

1. **Unique Indexes**: Prevent duplicate emails and usernames
2. **Query Indexes**: Speed up common queries (category, status, dates)
3. **Compound Indexes**: Optimize multi-field queries (auction_id + amount)
4. **Descending Indexes**: Optimize sorting by date/amount

### Data Growth

- **Users**: Slow growth, small documents
- **Auctions**: Moderate growth, medium documents
- **Bids**: Fast growth, small documents (most active collection)

### Optimization Tips

1. Use projection to limit returned fields
2. Implement pagination for large result sets
3. Cache frequently accessed data
4. Archive old closed auctions periodically
5. Monitor index usage and query performance

## Sample Data

### User Document
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "email": "john@example.com",
  "username": "johndoe",
  "password_hash": "$2b$12$KIXxLVxT5UWJQC.zGdz0.eH8Jf9vZ...",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Auction Document
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "title": "Vintage Camera",
  "description": "Rare vintage camera in excellent condition",
  "category": "Electronics",
  "starting_price": 100.0,
  "current_price": 150.0,
  "start_date": ISODate("2024-01-20T10:00:00Z"),
  "end_date": ISODate("2024-01-27T10:00:00Z"),
  "owner_id": "507f1f77bcf86cd799439011",
  "status": "active",
  "created_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Bid Document
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "auction_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439014",
  "amount": 150.0,
  "timestamp": ISODate("2024-01-16T15:30:00Z")
}
```
