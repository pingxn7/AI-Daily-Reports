#!/bin/bash
# 每日健康检查脚本 - 可以添加到 crontab 中每天运行

cd "$(dirname "$0")/.."

echo "==================================="
echo "AI News Collector - 每日健康检查"
echo "==================================="
echo ""
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查服务是否运行
if [ -f "logs/app.pid" ]; then
    PID=$(cat logs/app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务运行正常 (PID: $PID)"
    else
        echo "❌ 服务未运行，正在重启..."
        ./scripts/start.sh
    fi
else
    echo "❌ 服务未运行，正在启动..."
    ./scripts/start.sh
fi

echo ""
echo "==================================="
echo "检查完成"
echo "==================================="
