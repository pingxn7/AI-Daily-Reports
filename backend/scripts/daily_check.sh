#!/bin/bash
# 每日自动检查脚本 - 可以添加到 crontab 中
# 建议每天运行一次，确保服务正常

cd "$(dirname "$0")/.."

LOG_FILE="logs/daily_check_$(date +%Y%m%d).log"

{
    echo "=================================="
    echo "每日自动检查 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=================================="
    echo ""

    # 1. 检查服务状态
    echo "1. 检查服务状态..."
    if [ -f "logs/app.pid" ]; then
        PID=$(cat logs/app.pid)
        if ps -p $PID > /dev/null 2>&1; then
            echo "   ✅ 服务运行正常 (PID: $PID)"
        else
            echo "   ❌ 服务未运行，正在重启..."
            ./scripts/start.sh
            if [ $? -eq 0 ]; then
                echo "   ✅ 服务重启成功"
            else
                echo "   ❌ 服务重启失败，请手动检查"
            fi
        fi
    else
        echo "   ❌ 服务未运行，正在启动..."
        ./scripts/start.sh
    fi
    echo ""

    # 2. 检查调度器
    echo "2. 检查调度器状态..."
    SCHEDULER_STATUS=$(curl -s http://localhost:8000/api/scheduler/status 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "   ✅ 调度器运行正常"
        echo "$SCHEDULER_STATUS" | python3 -m json.tool 2>/dev/null | head -10
    else
        echo "   ❌ 无法连接到调度器"
    fi
    echo ""

    # 3. 检查数据库
    echo "3. 检查数据库状态..."
    ./venv/bin/python -c "
from app.database import SessionLocal
from sqlalchemy import text
try:
    db = SessionLocal()
    db.execute(text('SELECT 1'))
    db.close()
    print('   ✅ 数据库连接正常')
except Exception as e:
    print(f'   ❌ 数据库连接失败: {e}')
" 2>/dev/null
    echo ""

    # 4. 检查最近的日报
    echo "4. 检查最近的日报..."
    ./venv/bin/python -c "
from app.database import SessionLocal
from app.models.daily_summary import DailySummary
from datetime import date, timedelta
db = SessionLocal()
yesterday = date.today() - timedelta(days=1)
summary = db.query(DailySummary).filter(DailySummary.date == yesterday).first()
if summary:
    print(f'   ✅ 昨日日报已生成')
    print(f'   • 日期: {summary.date}')
    print(f'   • 推文数: {summary.tweet_count}')
    print(f'   • 邮件状态: {\"已发送\" if summary.email_sent_at else \"未发送\"}')
else:
    print(f'   ⚠️  昨日日报未生成')
db.close()
" 2>/dev/null
    echo ""

    # 5. 检查日志错误
    echo "5. 检查最近的错误日志..."
    ERROR_COUNT=$(grep -i "error\|fail" logs/app.log 2>/dev/null | tail -24h | wc -l)
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "   ⚠️  发现 $ERROR_COUNT 个错误，最近的错误："
        grep -i "error\|fail" logs/app.log 2>/dev/null | tail -5
    else
        echo "   ✅ 没有发现错误"
    fi
    echo ""

    # 6. 检查磁盘空间
    echo "6. 检查磁盘空间..."
    DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        echo "   ⚠️  磁盘使用率: ${DISK_USAGE}% (建议清理)"
    else
        echo "   ✅ 磁盘使用率: ${DISK_USAGE}%"
    fi
    echo ""

    echo "=================================="
    echo "检查完成 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=================================="

} | tee "$LOG_FILE"

# 如果有错误，可以发送通知（可选）
# 这里可以添加邮件通知或其他告警机制
