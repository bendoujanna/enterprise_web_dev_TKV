# Mobile Money SMS Transaction API Documentation

## Overview

This REST API provides secure access to mobile money SMS transaction data. The API supports full CRUD operations (Create, Read, Update, Delete) with Basic Authentication for security.

**Base URL:** `http://localhost:8000`

**Authentication:** Basic Authentication (username:password encoded in base64)

**Content Type:** `application/json`

---

## Authentication

All endpoints require Basic Authentication. Include credentials in the `Authorization` header:

```
Authorization: Basic base64(username:password)
```

### Valid Credentials

| Username | Password     |
|----------|--------------|
| admin    | password123  |
| user     | userpass     |

### Example Authentication Header

```bash
# Linux/Mac
echo -n "admin:password123" | base64
# Output: YWRtaW46cGFzc3dvcmQxMjM=

# Use in request:
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

---

## Endpoints

### 1. List All Transactions

**Endpoint:** `GET /transactions`

**Description:** Retrieve all SMS transactions from the database

**Authentication:** Required

**Request Example:**

```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "count": 20,
  "data": [
    {
    "id": "6",
    "type": "SEND",
    "amount": 10000.0,
    "sender": "You",
    "receiver": "Samuel Carter (250791666666)",
    "timestamp": "2024-05-11T20:34:55.316000",
    "status": "completed"
  },
  {
    "id": "7",
    "type": "SEND",
    "amount": 1000.0,
    "sender": "You",
    "receiver": "Samuel Carter (250790777777)",
    "timestamp": "2024-05-12T03:47:40.264000",
    "status": "completed"
  },
  ]
}
```

**Error Responses:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Unauthorized | `{"error": "Unauthorized", "message": "Invalid or missing credentials"}` |

---

### 2. Get Specific Transaction

**Endpoint:** `GET /transactions/{id}`

**Description:** Retrieve a single transaction by its ID

**Authentication:** Required

**URL Parameters:**
- `id` (string, required): Transaction ID

**Request Example:**

```bash
curl -X GET http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "1",
    "type": "SEND",
    "amount": 5000.0,
    "sender": "You",
    "receiver": "+250788654321",
    "timestamp": "2024-01-15T10:30:00",
    "status": "completed"
  }
}
```

**Error Responses:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Unauthorized | `{"error": "Unauthorized", "message": "Invalid or missing credentials"}` |
| 404 | Not Found | `{"error": "Not Found", "message": "Transaction with ID X not found"}` |

---

### 3. Create New Transaction

**Endpoint:** `POST /transactions`

**Description:** Create a new SMS transaction record

**Authentication:** Required

**Request Body Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Transaction type (SEND, RECEIVE, AIRTIME, WITHDRAW, DEPOSIT) |
| amount | number | Yes | Transaction amount |
| sender | string | Yes | Sender phone number or agent ID |
| receiver | string | Yes | Receiver phone number or agent ID |
| timestamp | string | No | ISO 8601 timestamp (auto-generated if not provided) |
| status | string | No | Transaction status (default: "pending") |

**Request Example:**

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SEND",
    "amount": 15000,
    "sender": "You",
    "receiver": "Robert Brown 23478",
    "status": "completed"
  }'
```

**Success Response (201 Created):**

```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "id": "21",
    "type": "SEND",
    "amount": 15000,
    "sender": "You",
    "receiver": "Robert Brown 23478",
    "timestamp": "2024-01-25T12:30:45.123456",
    "status": "completed"
  }
}
```

**Error Responses:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 400 | Bad Request | `{"error": "Bad Request", "message": "Missing required fields: type, amount"}` |
| 401 | Unauthorized | `{"error": "Unauthorized", "message": "Invalid or missing credentials"}` |

---

### 4. Update Transaction

**Endpoint:** `PUT /transactions/{id}`

**Description:** Update an existing transaction record

**Authentication:** Required

**URL Parameters:**
- `id` (string, required): Transaction ID to update

**Request Body:** Any transaction fields to update (except `id`)

**Request Example:**

```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 6000,
    "status": "verified"
  }'
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": {
    "id": "1",
    "type": "SEND",
    "amount": 6000,
    "sender": "You",
    "receiver": "Robert Brown 23478",
    "timestamp": "2024-01-15T10:30:00",
    "status": "verified"
  }
}
```

**Error Responses:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 400 | Bad Request | `{"error": "Bad Request", "message": "Invalid JSON in request body"}` |
| 401 | Unauthorized | `{"error": "Unauthorized", "message": "Invalid or missing credentials"}` |
| 404 | Not Found | `{"error": "Not Found", "message": "Transaction with ID X not found"}` |

---

### 5. Delete Transaction

**Endpoint:** `DELETE /transactions/{id}`

**Description:** Delete a transaction record

**Authentication:** Required

**URL Parameters:**
- `id` (string, required): Transaction ID to delete

**Request Example:**

```bash
curl -X DELETE http://localhost:8000/transactions/20 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Transaction 20 deleted successfully",
  "deleted": {
    "id": "20",
    "type": "RECEIVE",
    "amount": 8500.0,
    "sender": "You",
    "receiver": "Robert Brown 23478",
    "timestamp": "2024-01-23T16:00:00",
    "status": "completed"
  }
}
```

**Error Responses:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Unauthorized | `{"error": "Unauthorized", "message": "Invalid or missing credentials"}` |
| 404 | Not Found | `{"error": "Not Found", "message": "Transaction with ID X not found"}` |

---

## Error Codes Summary

| Status Code | Meaning |
|-------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request body or missing required fields |
| 401 | Unauthorized - Invalid or missing authentication credentials |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server-side error |

---

## Transaction Types

| Type | Description |
|------|-------------|
| SEND | Money sent to another user |
| RECEIVE | Money received from another user |
| AIRTIME | Airtime purchase |
| WITHDRAW | Cash withdrawal from agent |
| DEPOSIT | Cash deposit via agent |

---

## Testing with Postman

### 1. Set Up Authentication

1. Create a new request in Postman
2. Go to the **Authorization** tab
3. Select **Basic Auth** as type
4. Enter username: `admin`
5. Enter password: `password123`

### 2. Test GET Request

- Method: `GET`
- URL: `http://localhost:8000/transactions`
- Headers: Authorization is automatically added
- Send request

### 3. Test POST Request

- Method: `POST`
- URL: `http://localhost:8000/transactions`
- Headers: 
  - Authorization: Basic Auth (auto-added)
  - Content-Type: `application/json`
- Body (raw JSON):
```json
{
  "type": "SEND",
  "amount": 15000,
  "sender": "You",
  "receiver": "Samuel Carter 45355"
}
```

---

## Testing with curl

All test commands are available in `api/test_api.sh`. Run the API server first, then execute:

```bash
cd api
./test_api.sh
```

---

## Security Notes

### Basic Authentication Limitations

**Why Basic Auth is Weak:**

1. **Credentials in Every Request:** Username and password are sent with every request, increasing exposure
2. **Base64 is NOT Encryption:** Base64 encoding is easily reversible - credentials are essentially plain text
3. **No Built-in Expiration:** Credentials don't expire unless manually changed
4. **Vulnerable to Man-in-the-Middle:** Without HTTPS, credentials can be intercepted
5. **No Token Revocation:** Can't invalidate specific sessions without changing passwords

### Recommended Alternatives

#### 1. JWT (JSON Web Tokens)
- **Pros:** Stateless, includes expiration, can carry user info
- **Use Case:** Modern web/mobile apps
- **Example Flow:**
  1. User logs in with credentials
  2. Server returns JWT token
  3. Client includes token in subsequent requests
  4. Token expires after set time

#### 2. OAuth 2.0
- **Pros:** Industry standard, supports third-party login, granular permissions
- **Use Case:** Apps requiring third-party integration (Google, Facebook login)
- **Example Flow:**
  1. User authorizes via OAuth provider
  2. App receives access token
  3. Token used for API requests
  4. Refresh tokens for extended sessions

#### 3. API Keys
- **Pros:** Simple, can be rotated, different keys for different clients
- **Use Case:** Server-to-server communication, public APIs
- **Example Flow:**
  1. Generate API key for client
  2. Client includes key in header
  3. Server validates key against database

### Best Practices for Production

1. **Always use HTTPS** to encrypt credentials in transit
2. **Implement rate limiting** to prevent brute force attacks
3. **Use strong password policies** (minimum length, complexity requirements)
4. **Log authentication attempts** to detect suspicious activity
5. **Implement account lockout** after failed login attempts
6. **Use password hashing** (bcrypt, Argon2) to store credentials
7. **Add CORS policies** to restrict which domains can access your API
8. **Implement API versioning** for backward compatibility

---

## Data Structures & Algorithms

The API uses efficient data structures for transaction lookups:

### Dictionary Lookup (O(1))
The API maintains transactions in a dictionary (hash map) for constant-time lookups:

```python
transaction_dict = {
    "1": {...},
    "2": {...},
    "3": {...}
}

# O(1) lookup
transaction = transaction_dict.get("1")
```

### Performance Comparison

See `dsa/search_comparison.py` for detailed analysis comparing:
- **Linear Search:** O(n) - iterates through all transactions
- **Dictionary Lookup:** O(1) - direct hash table access

**Results:** Dictionary lookup is ~215.06x faster for 20 records, but scales dramatically better with larger datasets.

---

## Licence

This project is developed for educational purposes as part of the Enterprise Web Development Formative.
