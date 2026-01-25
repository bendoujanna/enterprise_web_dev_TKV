# Task 3: JSON Data Modeling
## MoMo SMS Processing System


## 1. Introduction
This JSON data modeling document outlines the serialization strategy for the MoMo SMS transaction processing system. Based on the ERD designed in Task 1, these JSON schemas represent how relational database entities are transformed into JSON format for API responses and data exchange.

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
    "user_id": "U1001",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "256712345678",
    "email": "john.doe@example.com",
    "registration_date": "2024-01-15T10:30:00Z",
    "account_status": "active",
    "balance": 150000.50
  }
}
``` 

### 2.2 Transaction Category
```json
{
  "transaction_category": {
    "category_id": "CAT001",
    "category_name": "Money Transfer",
    "description": "Person-to-person money transfer",
    "transaction_fee": 500.00,
    "min_amount": 1000.00,
    "max_amount": 5000000.00
  }
}
```

### 2.3 Agent Information
```json
{
  "agent": {
    "agent_id": "AGT001",
    "agent_name": "Nakasero Mobile Money Point",
    "phone": "256712345679",
    "location": "Kampala, Central Division",
    "status": "active",
    "registration_date": "2024-01-10T09:00:00Z",
    "daily_limit": 10000000.00,
    "transactions_today": 45,
    "commission_rate": 0.015
  }
}
```

### 2.4 System Log
```json
{
  "system_log": {
    "log_id": "LOG20240125001",
    "transaction_id": "TXN20240125001",
    "timestamp": "2024-01-25T14:30:45Z",
    "log_level": "INFO",
    "action": "transaction_processed",
    "status": "success",
    "user_id": "U1001",
    "ip_address": "192.168.1.100",
    "user_agent": "MoMoApp/2.1.0 iOS/15.4",
    "processing_time_ms": 245,
    "details": "Transaction completed successfully, SMS sent to both parties",
    "error_code": null,
    "stack_trace": null
  }
}
```

### 2.5 Complete Transaction (Complex Example)
This example demonstrates a fully nested transaction object with all related data:

```json
{
  "complete_transaction": {
    "transaction_summary": {
      "transaction_id": "TXN20240125001",
      "reference_id": "REF7A83B9C",
      "amount": 100000.00,
      "currency": "UGX",
      "transaction_date": "2024-01-25T14:30:45Z",
      "status": "completed",
      "description": "School fees payment",
      "transaction_type": "money_transfer"
    },
    "sender_details": {
      "user_id": "U1001",
      "full_name": "John Doe",
      "phone_number": "256712345678"
    },
    "receiver_details": {
      "user_id": "U1002",
      "full_name": "Jane Smith",
      "phone_number": "256712345680"
    },
    "financial_details": {
      "principal_amount": 100000.00,
      "transaction_fee": 500.00,
      "total_debit": 100500.00
    }
  }
}
```
## 3. SQL-to-JSON Mapping

| SQL Table | SQL Column | JSON Object | JSON Field | Data Type | Notes |
|-----------|------------|-------------|------------|-----------|-------|
| users | user_id | user | user_id | string | Primary key |
| users | first_name | user | firstName | string | camelCase in JSON |
| users | phone_number | user | phoneNumber | string | E.164 format |
| users | balance | user | balance | number | Decimal as number |
| transactions | transaction_id | transaction | transactionId | string | Unique identifier |
| transactions | amount | transaction | amount | number | Transaction value |
| transactions | status | transaction | status | string | completed/pending/failed |
| transaction_category | category_name | category | name | string | Payment type |
| agents | agent_name | agent | agentName | string | Display name |
| system_logs | log_timestamp | systemLog | timestamp | string | ISO 8601 format |
| locations | district | user.location | district | string | Nested object |

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