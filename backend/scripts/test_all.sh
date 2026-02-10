#!/bin/bash
# 日报邮件功能 - 一键测试脚本

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     日报邮件查看详情功能 - 一键测试                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 进入项目目录
cd "$(dirname "$0")/.."

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 1: 生成邮件预览"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/preview_email.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 2: 验证邮件内容"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "email_preview.html" ]; then
    echo "✓ 邮件预览文件已生成"

    # 检查关键内容
    if grep -q "查看完整详情" email_preview.html; then
        echo "✓ 包含 '查看完整详情' 按钮"
    else
        echo "✗ 缺少 '查看完整详情' 按钮"
    fi

    if grep -q "在线查看完整报告" email_preview.html; then
        echo "✓ 包含 '在线查看完整报告' 按钮"
    else
        echo "✗ 缺少 '在线查看完整报告' 按钮"
    fi

    if grep -q "浏览历史日报" email_preview.html; then
        echo "✓ 包含 '浏览历史日报' 链接"
    else
        echo "✗ 缺少 '浏览历史日报' 链接"
    fi

    if grep -q "localhost:3000/summary" email_preview.html; then
        echo "✓ 包含详情页 URL"
    else
        echo "✗ 缺少详情页 URL"
    fi
else
    echo "✗ 邮件预览文件未生成"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 3: 检查配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f ".env" ]; then
    echo "✓ .env 文件存在"

    if grep -q "FRONTEND_URL" .env; then
        FRONTEND_URL=$(grep "FRONTEND_URL" .env | cut -d '=' -f2)
        echo "✓ FRONTEND_URL: $FRONTEND_URL"
    else
        echo "⚠ FRONTEND_URL 未配置"
    fi

    if grep -q "RESEND_API_KEY" .env && [ -n "$(grep "RESEND_API_KEY" .env | cut -d '=' -f2)" ]; then
        echo "✓ RESEND_API_KEY 已配置"
    else
        echo "⚠ RESEND_API_KEY 未配置（可选）"
    fi
else
    echo "✗ .env 文件不存在"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 4: 检查文档"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

docs=(
    "IMPLEMENTATION_COMPLETE.md"
    "EMAIL_DETAIL_LINK_GUIDE.md"
    "EMAIL_FEATURE_SUMMARY.md"
    "QUICK_REFERENCE_EMAIL_LINKS.md"
    "VISUAL_EXAMPLE.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✓ $doc"
    else
        echo "✗ $doc (缺失)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 5: 检查脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

scripts=(
    "scripts/preview_email.py"
    "scripts/test_email_with_links.py"
    "scripts/demo_email_feature.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "✓ $script"
    else
        echo "✗ $script (缺失)"
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     测试完成！                                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 查看邮件预览:"
echo "   open email_preview.html"
echo ""
echo "📧 发送测试邮件:"
echo "   python scripts/test_email_with_links.py"
echo ""
echo "📚 查看文档:"
echo "   • IMPLEMENTATION_COMPLETE.md - 实现总结"
echo "   • QUICK_REFERENCE_EMAIL_LINKS.md - 快速参考"
echo ""
