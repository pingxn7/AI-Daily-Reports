#!/bin/bash
# 一键显示当前任务和快速操作指南

clear

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    AI News Collector - 当前状态                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 检查 API 服务器状态
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ API 服务器: 运行中"
else
    echo "❌ API 服务器: 未运行"
    echo "   启动命令: ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 获取系统指标
if curl -s http://localhost:8000/api/metrics > /dev/null 2>&1; then
    METRICS=$(curl -s http://localhost:8000/api/metrics)
    TOTAL_ACCOUNTS=$(echo "$METRICS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('scheduler', {}).get('jobs', [])))" 2>/dev/null || echo "N/A")

    echo "📊 系统统计:"
    echo "   • 监控账号数: $(curl -s http://localhost:8000/api/accounts | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "N/A")"
    echo "   • 总推文数: $(echo "$METRICS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_tweets', 'N/A'))" 2>/dev/null || echo "N/A")"
    echo "   • AI 相关推文: $(echo "$METRICS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('ai_related_tweets', 'N/A'))" 2>/dev/null || echo "N/A")"
    echo "   • 每日摘要数: $(echo "$METRICS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_summaries', 'N/A'))" 2>/dev/null || echo "N/A")"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "⏰ 定时任务:"
echo "   • 推文收集: 每 2 小时"
echo "   • 邮件推送: 每天上午 8:00 (北京时间)"
echo "   • 收件人: pingxn7@gmail.com"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📋 待办任务:"
echo ""
echo "   ⏳ 添加 28 个新账号"
echo "      需要手动获取 user_id 后批量导入"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🚀 快速操作:"
echo ""
echo "   1️⃣  添加账号 (3 步完成):"
echo "      • 访问: https://tweeterid.com/"
echo "      • 编辑: nano scripts/user_ids_to_import.txt"
echo "      • 导入: ./venv/bin/python scripts/import_user_ids.py"
echo ""
echo "   2️⃣  查看状态:"
echo "      python scripts/check_status.py"
echo ""
echo "   3️⃣  手动收集推文:"
echo "      python scripts/manual_collect.py"
echo ""
echo "   4️⃣  测试邮件:"
echo "      python scripts/test_email.py"
echo ""
echo "   5️⃣  查看帮助:"
echo "      ./scripts/show_add_tools.sh"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📚 文档:"
echo "   • 快速参考: cat scripts/README_ADD_ACCOUNTS.md"
echo "   • 完整指南: cat scripts/QUICK_START_ADD_ACCOUNTS.md"
echo "   • 总结文档: cat SUMMARY_AND_NEXT_STEPS.md"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🌐 Web 访问:"
echo "   • API 文档: http://localhost:8000/docs"
echo "   • 健康检查: http://localhost:8000/api/health"
echo "   • 系统指标: http://localhost:8000/api/metrics"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "💡 提示: 运行 './scripts/dashboard.sh' 可随时查看此面板"
echo ""
