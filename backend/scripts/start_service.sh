#!/bin/bash
# 启动 AI News Collector 后台服务
# 包含定时任务：每2小时收集推文，每天早上8点发送日报

cd "$(dirname "$0")/.."

echo "=================================="
echo "AI News Collector - 启动服务"
echo "=================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "   请先运行: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo "   请复制 .env.example 并配置必要的环境变量"
    exit 1
fi

echo "✓ 环境检查通过"
echo ""

# 显示配置信息
echo "📋 服务配置:"
source venv/bin/activate
python3 -c "
from app.config import settings
print(f'  API 地址: http://{settings.api_host}:{settings.api_port}')
print(f'  时区: {settings.schedule_timezone}')
print(f'  推文收集: {settings.schedule_tweet_collection_cron}')
print(f'  日报发送: {settings.schedule_daily_summary_cron} (每天早上8点)')
print(f'  收件人: {settings.email_to}')
print(f'  邮件功能: {\"启用\" if settings.enable_email else \"禁用\"}')
"
echo ""

echo "=================================="
echo "启动服务..."
echo "=================================="
echo ""

# 启动 FastAPI 应用
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 如果需要后台运行，使用以下命令：
# nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/app.log 2>&1 &
# echo "服务已在后台启动，PID: $!"
# echo "日志文件: logs/app.log"
