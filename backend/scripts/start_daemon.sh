#!/bin/bash
# 启动 AI News Collector 后台服务（守护进程模式）

cd "$(dirname "$0")/.."

echo "=================================="
echo "AI News Collector - 后台启动"
echo "=================================="
echo ""

# 创建日志目录
mkdir -p logs

# 检查是否已经在运行
if [ -f "logs/app.pid" ]; then
    PID=$(cat logs/app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  服务已在运行 (PID: $PID)"
        echo "   如需重启，请先运行: ./scripts/stop_service.sh"
        exit 1
    fi
fi

# 启动服务
echo "正在启动服务..."
nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/app.log 2>&1 &
PID=$!
echo $PID > logs/app.pid

sleep 2

# 检查是否启动成功
if ps -p $PID > /dev/null 2>&1; then
    echo ""
    echo "✅ 服务启动成功！"
    echo ""
    echo "📋 服务信息:"
    echo "  PID: $PID"
    echo "  API: http://localhost:8000"
    echo "  文档: http://localhost:8000/docs"
    echo "  日志: logs/app.log"
    echo ""
    echo "📅 定时任务:"
    echo "  • 每2小时收集推文"
    echo "  • 每天早上8点（北京时间）发送日报到 pingxn7@gmail.com"
    echo ""
    echo "💡 管理命令:"
    echo "  查看日志: tail -f logs/app.log"
    echo "  停止服务: ./scripts/stop_service.sh"
    echo "  查看状态: ./scripts/check_service.sh"
    echo ""
else
    echo "❌ 服务启动失败"
    echo "   请查看日志: cat logs/app.log"
    rm -f logs/app.pid
    exit 1
fi
