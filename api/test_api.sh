#!/bin/bash

# Test script for Mobile Money SMS Transaction API
# Run the API server first: cd api && python3 server.py

API_URL="http://localhost:8000"
AUTH="admin:password123"

echo "======================================"
echo "Mobile Money API Test Suite"
echo "======================================"

echo -e "\n1. Testing GET /transactions (List All) - WITH AUTH"
curl -X GET "$API_URL/transactions" \
  -H "Authorization: Basic $(echo -n $AUTH | base64)" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n2. Testing GET /transactions (List All) - WITHOUT AUTH (Should Fail)"
curl -X GET "$API_URL/transactions" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n3. Testing GET /transactions/1 (Get Specific Transaction)"
curl -X GET "$API_URL/transactions/1" \
  -H "Authorization: Basic $(echo -n $AUTH | base64)" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n4. Testing POST /transactions (Create New)"
curl -X POST "$API_URL/transactions" \
  -H "Authorization: Basic $(echo -n $AUTH | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SEND",
    "amount": 15000,
    "sender": "+250788111222",
    "receiver": "+250788333444",
    "status": "completed"
  }' \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n5. Testing PUT /transactions/1 (Update Transaction)"
curl -X PUT "$API_URL/transactions/1" \
  -H "Authorization: Basic $(echo -n $AUTH | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 6000,
    "status": "verified"
  }' \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n6. Testing DELETE /transactions/20 (Delete Transaction)"
curl -X DELETE "$API_URL/transactions/20" \
  -H "Authorization: Basic $(echo -n $AUTH | base64)" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n7. Testing Invalid Authentication"
curl -X GET "$API_URL/transactions" \
  -H "Authorization: Basic $(echo -n 'wrong:credentials' | base64)" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n======================================"
echo "Test Suite Complete"
echo "======================================"
