#!/bin/bash
# 停止 AI News Collector 服务

cd "$(dirname "$0")/.."

echo "=================================="
echo "AI News Collector - 停止服务"
echo "=================================="
echo ""

if [ ! -f "logs/app.pid" ]; then
    echo "⚠️  服务未运行（未找到 PID 文件）"
    exit 0
fi

PID=$(cat logs/app.pid)

if ! ps -p $PID > /dev/null 2>&1; then
    echo "⚠️  服务未运行（进程不存在）"
    rm -f logs/app.pid
    exit 0
fi

echo "正在停止服务 (PID: $PID)..."
kill $PID

# 等待进程结束
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务已停止"
        rm -f logs/app.pid
        exit 0
    fi
    sleep 1
done

# 如果还没停止，强制终止
echo "⚠️  正常停止失败，强制终止..."
kill -9 $PID
rm -f logs/app.pid
echo "✅ 服务已强制停止"
