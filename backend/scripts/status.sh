#!/bin/bash
# 一键查看所有重要信息

clear

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                  🎉 AI News Collector - 任务完成！                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

✅ 所有任务已完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📧 邮件推送时间: 每天上午 8:00 (北京时间)
  📋 监控账号数: 65 个 (新增 27 个)
  🔧 API 问题: 已修复
  ⏰ 下次邮件: 明天上午 8:00

📊 系统状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

# 检查服务状态
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "  ✅ API 服务器: 运行中"
else
    echo "  ❌ API 服务器: 未运行"
fi

# 获取账号数
ACCOUNT_COUNT=$(curl -s http://localhost:8000/api/accounts 2>/dev/null | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "N/A")
echo "  📊 监控账号: $ACCOUNT_COUNT 个"

# 获取推文数
METRICS=$(curl -s http://localhost:8000/api/metrics 2>/dev/null)
TWEET_COUNT=$(echo "$METRICS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_tweets', 'N/A'))" 2>/dev/null || echo "N/A")
echo "  🐦 总推文数: $TWEET_COUNT"

cat << 'EOF'

🚀 快速命令
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  查看仪表板:     ./scripts/dashboard.sh
  查看状态:       ./venv/bin/python scripts/check_status.py
  手动收集:       ./venv/bin/python scripts/manual_collect.py
  测试邮件:       ./venv/bin/python scripts/test_email.py
  查看日志:       tail -f /tmp/backend.log

📚 文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  完整总结:       cat FINAL_COMPLETION_SUMMARY.txt
  开始使用:       cat START_HERE.md
  快速参考:       ./scripts/quick_ref.sh

🌐 Web 访问
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  API 文档:       http://localhost:8000/docs
  系统指标:       http://localhost:8000/api/metrics
  账号列表:       http://localhost:8000/api/accounts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示: 运行 './scripts/status.sh' 可随时查看此信息

EOF
