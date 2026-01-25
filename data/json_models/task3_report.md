# Task 3: JSON Data Modeling
## MoMo SMS Processing System


## 1. Introduction
This JSON data modeling document outlines the serialization strategy for the MoMo SMS transaction processing system. Based on the ERD designed in Task 1, these JSON schemas represent how relational database entities are transformed into JSON format for API responses and data exchange.

**Important:** All JSON schemas exactly match the actual database structure with:
- **Integer IDs** (not strings) matching database AUTO_INCREMENT columns
- **Rwandan phone formats** (+250) as stored in the database  
- **Correct ENUM values** (COMPLETED, PERSON, INFO, etc.)
- **Removed extra fields** not present in database schema
- **Added missing fields** (account_code, user_type, reference_code, etc.)


The design follows RESTful API best practices, with nested objects for related data to reduce client-side API calls. Each JSON structure maintains referential integrity while optimizing for mobile network efficiency - crucial for SMS-based systems in regions with limited bandwidth.

Key design decisions include:
- Using camelCase for JSON properties (vs snake_case in SQL)
- ISO 8601 timestamps for consistency
- Nested location data within user/agent objects
- Separate audit logs for transaction tracing
- Flexible `additional_data` fields for future expansion

These JSON models support the full transaction lifecycle from initiation through SMS notification, ensuring data consistency between the database and external systems.

## 2. JSON Schema Examples

### 2.1 User Object

```json
{
  "user": {
    "user_id": 1,
    "name": "Jean Damascene Nkusi",
    "phone_number": "+250788123456",
    "account_code": "ACC001",
    "user_type": "PERSON",
    "account_balance": 50000.00,
    "created_at": "2024-01-24T10:30:00Z"
  }
}
``` 

### 2.2 Transaction Category
```json
{
  "transaction_category": {
    "category_id": 1,
    "name": "Money Transfer",
    "code": "XFER",
    "description": "Person-to-person money transfer",
    "created_at": "2024-01-24T09:00:00Z"
  }
}
```



### 2.3 System Log
```json
{
  "system_log": {
    "log_id": 1,
    "user_id": 1,
    "transaction_id": "TXN20260124001",
    "log_date": "2024-01-24T14:30:46Z",
    "log_level": "INFO",
    "action": "TRANSACTION_CREATED",
    "message": "User initiated money transfer successfully"
  }
}
```

### 2.4 Complete Transaction (Complex Example)
This example demonstrates a fully nested transaction object with all related data:

```json
{
  "transaction": {
    "transaction_id": "TXN20260124001",
    "category_id": 1,
    "amount": 10000.00,
    "currency": "RWF",
    "transaction_date": "2024-01-24T14:30:45Z",
    "fee": 100.00,
    "balance_after": 39900.00,
    "status": "COMPLETED",
    "reference_code": "REF001",
    "description": "Money transfer to Marie",
    "created_at": "2024-01-24T14:30:45Z"
  },
  "parties": [
    {
      "party_id": 1,
      "user_id": 1,
      "name": "Jean Damascene Nkusi",
      "role": "SENDER",
      "phone_number": "+250788123456"
    },
    {
      "party_id": 2,
      "user_id": 2,
      "name": "Marie Claire Uwase",
      "role": "RECEIVER",
      "phone_number": "+250788234567"
    }
  ],
  "category": {
    "category_id": 1,
    "name": "Money Transfer",
    "code": "XFER"
  }
}
```
## 3. SQL-to-JSON Mapping

| SQL Table | SQL Column | JSON Object | JSON Field | Data Type | Notes |
|-----------|------------|-------------|------------|-----------|-------|
| users | user_id | user | user_id | integer | Primary key (INT) |
| users | name | user | name | string | Full name |
| users | phone_number | user | phoneNumber | string | E.164 format with + |
| users | account_code | user | accountCode | string | MoMo account identifier |
| users | user_type | user | userType | string | PERSON/MERCHANT/BANK/AGENT/SYSTEM |
| users | account_balance | user | accountBalance | number | Current balance |
| users | created_at | user | createdAt | string | ISO 8601 format |
| transactions | transaction_id | transaction | transactionId | string | Unique identifier |
| transactions | category_id | transaction | categoryId | integer | Foreign key to categories |
| transactions | amount | transaction | amount | number | Transaction value |
| transactions | currency | transaction | currency | string | RWF/USD/EUR |
| transactions | reference_code | transaction | referenceCode | string | External reference |
| transaction_categories | code | category | code | string | Short category code |
| system_logs | log_level | systemLog | logLevel | string | INFO/WARNING/ERROR/CRITICAL |
| transaction_parties | role | party | role | string | SENDER/RECEIVER/AGENT |

**Serialization Rules:**
1. SQL snake_case → JSON camelCase
2. DATETIME → ISO 8601 string
3. DECIMAL → JSON number
4. BOOLEAN → JSON boolean
5. NULL values are omitted from JSON responses

## 4. Implementation Notes

### 4.1 API Design Considerations
- **Endpoints**: RESTful endpoints follow `/api/v1/{resource}` pattern
- **Pagination**: List responses include `_next` and `_prev` links
- **Filtering**: Query parameters like `?status=completed&min_amount=10000`
- **Embedding**: Use `?_embed=user,agent` to include nested resources

### 4.2 Serialization Strategy
1. **Database → JSON**: Custom serializers transform SQL results to JSON
2. **Caching**: Frequently accessed objects cached in Redis as JSON
3. **Validation**: JSON Schema validation on API inputs
4. **Versioning**: API version in URL and JSON metadata

### 4.3 Performance Optimizations
- **Selective Fields**: Clients can request specific fields with `?fields=id,name,amount`
- **Compression**: JSON responses gzipped for mobile networks
- **Batch Operations**: Bulk transaction processing supported
- **WebSocket Updates**: Real-time transaction updates via WebSocket

### 4.4 Security Considerations
- **Sensitive Data**: Account numbers masked in JSON responses
- **Rate Limiting**: JSON error responses include retry-after headers
- **Audit Logs**: All API calls logged as JSON for analysis
- **Data Sanitization**: JSON inputs validated and sanitized