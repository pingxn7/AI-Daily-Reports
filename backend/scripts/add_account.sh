#!/bin/bash
# Quick script to add a Twitter account to monitoring

if [ "$#" -lt 2 ]; then
    echo "Usage: ./add_account.sh <username> <user_id> [display_name]"
    echo ""
    echo "Example:"
    echo "  ./add_account.sh karpathy 17919972 \"Andrej Karpathy\""
    echo ""
    echo "To find user_id, visit: https://tweeterid.com/"
    exit 1
fi

USERNAME=$1
USER_ID=$2
DISPLAY_NAME=${3:-$USERNAME}

echo "Adding account: @$USERNAME (ID: $USER_ID)"

# Check if server is running
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "Error: API server is not running"
    echo "Start it with: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    exit 1
fi

# Add account via API
RESPONSE=$(curl -s -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"username\": \"$USERNAME\",
    \"display_name\": \"$DISPLAY_NAME\",
    \"is_active\": true
  }")

echo "$RESPONSE" | python3 -m json.tool

if echo "$RESPONSE" | grep -q "\"id\""; then
    echo ""
    echo "✓ Successfully added @$USERNAME"
else
    echo ""
    echo "✗ Failed to add account"
fi
