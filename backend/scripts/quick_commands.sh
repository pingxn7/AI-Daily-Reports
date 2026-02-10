#!/bin/bash
# 快速参考指南 - 常用命令速查

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║           AI News Collector - 快速命令参考                       ║
╚══════════════════════════════════════════════════════════════════╝

📋 服务管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  启动服务:    ./scripts/start.sh
  停止服务:    ./scripts/stop_service.sh
  查看状态:    ./scripts/check_service.sh
  查看日志:    tail -f logs/app.log
  健康检查:    ./scripts/health_check.sh

📧 日报操作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  发送昨天日报:  ./venv/bin/python scripts/send_daily_report.py
  发送指定日期:  ./venv/bin/python scripts/send_daily_report.py 2026-02-08
  测试邮件:      ./venv/bin/python scripts/test_email.py
  生成日报:      ./venv/bin/python scripts/generate_daily_report.py

🐦 推文管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  手动收集:      ./venv/bin/python scripts/manual_collect.py
  生成摘要:      ./venv/bin/python scripts/manual_summary.py
  查看状态:      ./venv/bin/python scripts/check_status.py

🔍 监控调试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  系统测试:      ./venv/bin/python scripts/test_system.py
  调度器状态:    curl http://localhost:8000/api/scheduler/status
  API 文档:      open http://localhost:8000/docs

⏰ 定时任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  推文收集:      每2小时自动执行
  日报发送:      每天早上8点（北京时间）
  收件人:        pingxn7@gmail.com

📁 重要文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  配置文件:      .env
  日志文件:      logs/app.log
  进程ID:        logs/app.pid
  日报文件:      reports/

🔗 API 端点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  主页:          http://localhost:8000/
  API文档:       http://localhost:8000/docs
  调度器状态:    http://localhost:8000/api/scheduler/status
  日报列表:      http://localhost:8000/api/summaries

📚 文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  快速开始:      cat QUICK_START.md
  调度器指南:    cat SCHEDULER_GUIDE.md
  配置完成:      cat SETUP_COMPLETE.md
  快速参考:      ./scripts/quick_ref.sh

💡 提示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 服务会在后台持续运行
  • 每天早上8点自动发送日报到 pingxn7@gmail.com
  • 如果服务停止，运行 ./scripts/start.sh 重启
  • 查看实时日志: tail -f logs/app.log

EOF
