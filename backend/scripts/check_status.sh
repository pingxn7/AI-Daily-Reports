#!/bin/bash
# Twitter 账号监听系统 - 快速状态检查

echo "=================================="
echo "Twitter AI 新闻监听系统 - 状态检查"
echo "=================================="
echo ""

# 检查 API 服务器
echo "📡 检查 API 服务器..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ API 服务器运行正常"
else
    echo "❌ API 服务器未运行"
    echo "   启动命令: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi
echo ""

# 检查账号数量
echo "👥 检查监听账号..."
ACCOUNT_COUNT=$(curl -s http://localhost:8000/api/accounts 2>/dev/null | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ ! -z "$ACCOUNT_COUNT" ]; then
    echo "✅ 当前监听账号数: $ACCOUNT_COUNT"
else
    echo "❌ 无法获取账号信息"
fi
echo ""

# 检查系统指标
echo "📊 系统指标..."
curl -s http://localhost:8000/api/metrics 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"✅ 已收集推文: {data.get('total_tweets', 0)} 条\")
    print(f\"✅ AI 相关推文: {data.get('ai_related_tweets', 0)} 条\")
    print(f\"✅ 生成摘要: {data.get('total_summaries', 0)} 份\")

    scheduler = data.get('scheduler', {})
    if scheduler.get('running'):
        print(f\"✅ 调度器: 运行中\")
        jobs = scheduler.get('jobs', [])
        for job in jobs:
            print(f\"   - {job.get('name')}: {job.get('next_run')}\")
    else:
        print(f\"❌ 调度器: 未运行\")
except:
    print('❌ 无法获取系统指标')
" 2>/dev/null
echo ""

# 检查数据库
echo "💾 检查数据库..."
if psql -U pingxn7 -d ai_news -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ 数据库连接正常"
    TWEET_COUNT=$(psql -U pingxn7 -d ai_news -t -c "SELECT COUNT(*) FROM tweets;" 2>/dev/null | tr -d ' ')
    ACCOUNT_COUNT_DB=$(psql -U pingxn7 -d ai_news -t -c "SELECT COUNT(*) FROM monitored_accounts;" 2>/dev/null | tr -d ' ')
    echo "   - 数据库中的推文: $TWEET_COUNT 条"
    echo "   - 数据库中的账号: $ACCOUNT_COUNT_DB 个"
else
    echo "❌ 数据库连接失败"
fi
echo ""

echo "=================================="
echo "快速操作"
echo "=================================="
echo ""
echo "📝 添加账号:"
echo "   python scripts/add_accounts_interactive.py"
echo ""
echo "📋 查看账号列表:"
echo "   python scripts/add_accounts_interactive.py --list"
echo ""
echo "📊 查看详细指标:"
echo "   curl http://localhost:8000/api/metrics | python3 -m json.tool"
echo ""
echo "📚 查看 API 文档:"
echo "   open http://localhost:8000/docs"
echo ""
echo "=================================="
