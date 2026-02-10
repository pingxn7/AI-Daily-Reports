#!/bin/bash
# 一键启动 AI News Collector 服务
# 包含完整的环境检查和配置验证

cd "$(dirname "$0")/.."

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         AI News Collector - 自动启动脚本                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 1. 环境检查
echo "📋 步骤 1/5: 环境检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在"
    echo "   正在创建虚拟环境..."
    python3 -m venv venv
    echo "   正在安装依赖..."
    ./venv/bin/pip install -r requirements.txt
    echo "   ✓ 虚拟环境创建完成"
else
    echo "   ✓ 虚拟环境存在"
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在"
    echo "   请复制 .env.example 并配置必要的环境变量"
    exit 1
else
    echo "   ✓ .env 文件存在"
fi

# 检查数据库连接
echo "   检查数据库连接..."
./venv/bin/python -c "
from app.database import SessionLocal
from sqlalchemy import text
try:
    db = SessionLocal()
    db.execute(text('SELECT 1'))
    db.close()
    print('   ✓ 数据库连接正常')
except Exception as e:
    print(f'   ❌ 数据库连接失败: {e}')
    exit(1)
" || exit 1

echo ""

# 2. 配置验证
echo "📋 步骤 2/5: 配置验证"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./venv/bin/python -c "
from app.config import settings
print(f'   API 地址: http://{settings.api_host}:{settings.api_port}')
print(f'   时区: {settings.schedule_timezone}')
print(f'   邮件功能: {\"✓ 启用\" if settings.enable_email else \"✗ 禁用\"}')
print(f'   收件人: {settings.email_to}')
print(f'   推文收集: {settings.schedule_tweet_collection_cron}')
print(f'   日报发送: {settings.schedule_daily_summary_cron} (每天早上8点)')
"
echo ""

# 3. 检查是否已在运行
echo "📋 步骤 3/5: 检查服务状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "logs/app.pid" ]; then
    PID=$(cat logs/app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ⚠️  服务已在运行 (PID: $PID)"
        echo "   如需重启，请先运行: ./scripts/stop_service.sh"
        exit 0
    else
        rm -f logs/app.pid
    fi
fi
echo "   ✓ 服务未运行，可以启动"
echo ""

# 4. 创建必要的目录
echo "📋 步骤 4/5: 准备运行环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p logs
mkdir -p reports
echo "   ✓ 日志目录已创建"
echo "   ✓ 报告目录已创建"
echo ""

# 5. 启动服务
echo "📋 步骤 5/5: 启动服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   正在启动后台服务..."

nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/app.log 2>&1 &
PID=$!
echo $PID > logs/app.pid

sleep 3

# 验证启动
if ps -p $PID > /dev/null 2>&1; then
    echo "   ✓ 服务启动成功"
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    🎉 启动成功！                               ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 服务信息:"
    echo "   • PID: $PID"
    echo "   • API: http://localhost:8000"
    echo "   • 文档: http://localhost:8000/docs"
    echo "   • 日志: logs/app.log"
    echo ""
    echo "📅 定时任务:"
    echo "   • 每2小时自动收集推文"
    echo "   • 每天早上8点（北京时间）自动发送日报"
    echo "   • 收件人: pingxn7@gmail.com"
    echo ""
    echo "💡 管理命令:"
    echo "   • 查看日志: tail -f logs/app.log"
    echo "   • 查看状态: ./scripts/check_service.sh"
    echo "   • 停止服务: ./scripts/stop_service.sh"
    echo "   • 手动发送日报: ./venv/bin/python scripts/send_daily_report.py"
    echo ""
    echo "🔗 快速链接:"
    echo "   • 调度器状态: curl http://localhost:8000/api/scheduler/status"
    echo "   • 系统状态: ./venv/bin/python scripts/check_status.py"
    echo ""
else
    echo "   ❌ 服务启动失败"
    echo ""
    echo "请查看日志文件获取详细信息:"
    echo "   cat logs/app.log"
    echo ""
    rm -f logs/app.pid
    exit 1
fi
