#!/bin/bash
# 系统状态总览脚本

echo ""
echo "================================================================================"
echo "AI 新闻收集系统 - 当前状态"
echo "================================================================================"
echo ""

# 检查 API 服务器
echo "📡 API 服务器状态:"
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "   ✅ 运行中 (http://localhost:8000)"
    HEALTH=$(curl -s http://localhost:8000/api/health | jq -r '.status')
    echo "   状态: $HEALTH"
else
    echo "   ❌ 未运行"
    echo "   启动命令: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi
echo ""

# 检查监听账号
echo "👥 监听账号:"
ACCOUNT_COUNT=$(curl -s http://localhost:8000/api/accounts 2>/dev/null | jq 'length' 2>/dev/null)
if [ ! -z "$ACCOUNT_COUNT" ]; then
    echo "   总数: $ACCOUNT_COUNT 个"
    echo ""
    echo "   账号列表:"
    curl -s http://localhost:8000/api/accounts | jq -r '.[] | "   ✓ @\(.username) - \(.display_name)"' | sort
else
    echo "   ❌ 无法获取账号信息"
fi
echo ""

# 检查推文数量
echo "📝 收集的推文:"
TWEET_COUNT=$(curl -s http://localhost:8000/api/tweets 2>/dev/null | jq 'length' 2>/dev/null)
if [ ! -z "$TWEET_COUNT" ]; then
    echo "   总数: $TWEET_COUNT 条"
else
    echo "   ❌ 无法获取推文信息"
fi
echo ""

# 检查环境变量
echo "🔑 API 配置:"
if [ ! -z "$TWITTER_BEARER_TOKEN" ]; then
    TOKEN_LEN=${#TWITTER_BEARER_TOKEN}
    echo "   ✅ Twitter Bearer Token: 已配置 (长度: $TOKEN_LEN)"
else
    echo "   ⚠️  Twitter Bearer Token: 未配置"
    echo "      需要配置以自动获取 user_id"
fi
echo ""

# 待添加账号
echo "⏳ 待添加账号:"
PENDING_ACCOUNTS=(
    "aidangomez"
    "EpochAIResearch"
    "drfeifei"
    "geoffreyhinton"
    "gdb"
    "indigox"
    "jackclarkSF"
    "johnschulman2"
    "mustafasuleyman"
    "NoamShazeer"
    "OriolVinyalsML"
    "pabbeel"
    "rasbt"
    "SebastienBubeck"
    "soumithchintala"
    "woj_zaremba"
    "Yoshua_Bengio"
    "zephyr_z9"
    "_jasonwei"
    "lennysan"
    "thinkymachines"
)

# 检查哪些账号还未添加
PENDING_COUNT=0
for username in "${PENDING_ACCOUNTS[@]}"; do
    if ! curl -s http://localhost:8000/api/accounts 2>/dev/null | jq -r '.[].username' | grep -q "^${username}$"; then
        if [ $PENDING_COUNT -eq 0 ]; then
            echo "   还需添加 21 个账号:"
        fi
        PENDING_COUNT=$((PENDING_COUNT + 1))
        if [ $PENDING_COUNT -le 5 ]; then
            echo "   - @$username"
        fi
    fi
done

if [ $PENDING_COUNT -gt 5 ]; then
    echo "   - ... 还有 $((PENDING_COUNT - 5)) 个账号"
fi

if [ $PENDING_COUNT -eq 0 ]; then
    echo "   ✅ 所有账号已添加！"
fi
echo ""

# 下一步建议
echo "================================================================================"
echo "📋 下一步操作建议"
echo "================================================================================"
echo ""

if [ -z "$TWITTER_BEARER_TOKEN" ]; then
    echo "方案 1: 使用官方 X Developer API（推荐，最快）"
    echo "   1. 申请 X Developer API"
    echo "      访问: https://developer.twitter.com/"
    echo "      指南: cat HOW_TO_APPLY_X_API.md"
    echo ""
    echo "   2. 配置 Bearer Token"
    echo "      echo 'TWITTER_BEARER_TOKEN=你的token' >> .env"
    echo ""
    echo "   3. 测试 Token"
    echo "      python scripts/test_bearer_token.py"
    echo ""
    echo "   4. 自动获取并添加所有账号"
    echo "      python scripts/fetch_with_official_api.py"
    echo ""
    echo "方案 2: 手动获取 user_id"
    echo "   1. 访问 https://tweeterid.com/"
    echo "   2. 查询账号的 user_id"
    echo "   3. 使用脚本添加"
    echo "      ./scripts/add_one.sh username user_id \"Display Name\""
else
    echo "✅ Bearer Token 已配置！"
    echo ""
    echo "立即运行以下命令添加所有账号:"
    echo "   python scripts/fetch_with_official_api.py"
fi
echo ""

# 有用的命令
echo "================================================================================"
echo "🛠️  常用命令"
echo "================================================================================"
echo ""
echo "查看 API 文档:        open http://localhost:8000/docs"
echo "查看所有账号:        curl http://localhost:8000/api/accounts | jq"
echo "查看最新推文:        curl http://localhost:8000/api/tweets | jq"
echo "测试 Bearer Token:   python scripts/test_bearer_token.py"
echo "添加单个账号:        ./scripts/add_one.sh username user_id"
echo "查看完整指南:        cat NEXT_STEPS.md"
echo ""
echo "================================================================================"
echo ""
