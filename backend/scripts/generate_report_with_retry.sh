#!/bin/bash
# 自动重试生成日报脚本

cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate

echo "=================================="
echo "AI 日报生成器（自动重试版本）"
echo "=================================="
echo ""
echo "使用新的 System Prompt v2"
echo "来源: /Users/pingxn7/Desktop/AI_Twitter_Editor_System_Prompt_v2_FULL.md"
echo ""

MAX_RETRIES=5
RETRY_DELAY=30

for i in $(seq 1 $MAX_RETRIES); do
    echo "尝试 $i/$MAX_RETRIES..."
    
    if python scripts/generate_daily_report.py 2026-02-08 <<< "yes"; then
        echo ""
        echo "✅ 日报生成成功！"
        echo ""
        echo "查看日报："
        echo "  cat reports/ai_daily_report_2026-02-08.md"
        echo ""
        echo "发送邮件："
        echo "  python scripts/test_email.py"
        exit 0
    else
        if [ $i -lt $MAX_RETRIES ]; then
            echo "❌ 失败，等待 ${RETRY_DELAY} 秒后重试..."
            sleep $RETRY_DELAY
        fi
    fi
done

echo ""
echo "❌ 多次尝试后仍然失败"
echo "可能是 Anthropic API 暂时不可用"
echo "请稍后手动运行："
echo "  python scripts/generate_daily_report.py 2026-02-08"
exit 1
