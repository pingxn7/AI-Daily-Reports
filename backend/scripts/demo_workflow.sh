#!/bin/bash
# 完整工作流程演示脚本

echo ""
echo "================================================================================"
echo "🎯 AI 新闻收集系统 - 完整工作流程"
echo "================================================================================"
echo ""

# 检查当前目录
if [ ! -f "app/main.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    echo "   cd /Users/pingxn7/Desktop/x/backend"
    exit 1
fi

echo "📋 当前状态检查..."
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 检查 API 服务器
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ API 服务器运行中"
else
    echo "⚠️  API 服务器未运行"
    echo "   启动命令: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    echo ""
fi

# 检查账号数量
ACCOUNT_COUNT=$(curl -s http://localhost:8000/api/accounts 2>/dev/null | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ ! -z "$ACCOUNT_COUNT" ]; then
    echo "✅ 当前监听账号: $ACCOUNT_COUNT 个"
else
    echo "⚠️  无法获取账号信息"
fi

# 检查 Bearer Token
if [ ! -z "$TWITTER_BEARER_TOKEN" ]; then
    echo "✅ Twitter Bearer Token: 已配置"
else
    if grep -q "TWITTER_BEARER_TOKEN" .env 2>/dev/null; then
        echo "✅ Twitter Bearer Token: 已在 .env 文件中配置"
    else
        echo "⚠️  Twitter Bearer Token: 未配置"
    fi
fi

echo ""
echo "================================================================================"
echo "📝 下一步操作"
echo "================================================================================"
echo ""

# 检查是否需要添加账号
if [ "$ACCOUNT_COUNT" -lt "25" ]; then
    echo "建议添加更多账号以获得更全面的 AI 新闻覆盖"
    echo ""
    echo "方案 1: 使用官方 X Developer API（推荐）"
    echo "   1. 申请 API: https://developer.twitter.com/"
    echo "   2. 配置 Token: echo 'TWITTER_BEARER_TOKEN=你的token' >> .env"
    echo "   3. 运行脚本: python scripts/fetch_with_official_api.py"
    echo ""
    echo "方案 2: 手动添加"
    echo "   1. 访问: https://tweeterid.com/"
    echo "   2. 查询 user_id"
    echo "   3. 添加: ./scripts/add_one.sh username user_id \"Display Name\""
    echo ""
else
    echo "✅ 账号数量充足！"
    echo ""
fi

echo "================================================================================"
echo "🛠️  常用命令"
echo "================================================================================"
echo ""
echo "查看所有账号:"
echo "  curl http://localhost:8000/api/accounts | python3 -m json.tool"
echo ""
echo "查看最新推文:"
echo "  curl http://localhost:8000/api/tweets | python3 -m json.tool"
echo ""
echo "查看 API 文档:"
echo "  open http://localhost:8000/docs"
echo ""
echo "测试 Bearer Token:"
echo "  source venv/bin/activate && python scripts/test_bearer_token.py"
echo ""
echo "自动添加账号:"
echo "  source venv/bin/activate && python scripts/fetch_with_official_api.py"
echo ""
echo "================================================================================"
echo ""
