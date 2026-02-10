#!/bin/bash
# 检查 AI News Collector 服务状态

cd "$(dirname "$0")/.."

echo "=================================="
echo "AI News Collector - 服务状态"
echo "=================================="
echo ""

# 检查进程
if [ -f "logs/app.pid" ]; then
    PID=$(cat logs/app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务运行中"
        echo "  PID: $PID"
        echo "  API: http://localhost:8000"
        echo ""

        # 尝试获取调度器状态
        echo "📅 定时任务状态:"
        curl -s http://localhost:8000/api/scheduler/status 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "  无法获取调度器状态"
        echo ""

        # 显示最近日志
        echo "📝 最近日志 (最后10行):"
        echo "---"
        tail -10 logs/app.log 2>/dev/null || echo "  无日志文件"
        echo ""
    else
        echo "❌ 服务未运行（进程不存在）"
        rm -f logs/app.pid
    fi
else
    echo "❌ 服务未运行（未找到 PID 文件）"
fi

echo ""
echo "💡 管理命令:"
echo "  启动服务: ./scripts/start_daemon.sh"
echo "  停止服务: ./scripts/stop_service.sh"
echo "  查看日志: tail -f logs/app.log"
echo ""
