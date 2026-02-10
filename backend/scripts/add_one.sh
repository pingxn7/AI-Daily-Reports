#!/bin/bash
# 快速添加单个账号的脚本
# 用法: ./add_one.sh username user_id

if [ $# -lt 2 ]; then
    echo "用法: ./add_one.sh <username> <user_id> [display_name]"
    echo "示例: ./add_one.sh aidangomez 123456789 \"Aidan Gomez\""
    exit 1
fi

USERNAME=$1
USER_ID=$2
DISPLAY_NAME=${3:-$USERNAME}

echo "添加账号: @$USERNAME (ID: $USER_ID)"

curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"user_id\": \"$USER_ID\", \"display_name\": \"$DISPLAY_NAME\", \"is_active\": true}" \
  -w "\n"

echo ""
echo "完成！"
echo "查看所有账号: curl http://localhost:8000/api/accounts | jq"
