#!/bin/bash
# 日报邮件功能演示脚本

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     AI 行业日报 - 查看详情功能演示                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检查环境
echo "📋 步骤 1: 检查环境配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f ".env" ]; then
    echo "✓ .env 文件存在"

    if grep -q "FRONTEND_URL" .env; then
        FRONTEND_URL=$(grep "FRONTEND_URL" .env | cut -d '=' -f2)
        echo "✓ FRONTEND_URL: $FRONTEND_URL"
    else
        echo "✗ FRONTEND_URL 未配置"
    fi

    if grep -q "RESEND_API_KEY" .env; then
        echo "✓ RESEND_API_KEY 已配置"
    else
        echo "✗ RESEND_API_KEY 未配置"
    fi

    if grep -q "EMAIL_TO" .env; then
        EMAIL_TO=$(grep "EMAIL_TO" .env | cut -d '=' -f2)
        echo "✓ EMAIL_TO: $EMAIL_TO"
    else
        echo "✗ EMAIL_TO 未配置"
    fi
else
    echo "✗ .env 文件不存在"
    exit 1
fi
echo ""

# 激活虚拟环境
echo "📋 步骤 2: 激活虚拟环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 虚拟环境不存在"
    exit 1
fi
echo ""

# 生成邮件预览
echo "📋 步骤 3: 生成邮件预览"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/preview_email.py
if [ $? -eq 0 ]; then
    echo "✓ 邮件预览生成成功"
    echo "  文件位置: email_preview.html"
else
    echo "✗ 邮件预览生成失败"
    exit 1
fi
echo ""

# 询问是否发送测试邮件
echo "📋 步骤 4: 发送测试邮件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "是否发送测试邮件到 $EMAIL_TO? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python scripts/test_email_with_links.py
    if [ $? -eq 0 ]; then
        echo "✓ 测试邮件发送成功"
    else
        echo "✗ 测试邮件发送失败"
    fi
else
    echo "⊘ 跳过发送测试邮件"
fi
echo ""

# 打开预览
echo "📋 步骤 5: 打开邮件预览"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "是否在浏览器中打开邮件预览? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open email_preview.html
    echo "✓ 已在浏览器中打开预览"
else
    echo "⊘ 跳过打开预览"
fi
echo ""

# 显示测试链接
echo "📋 步骤 6: 测试链接"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TODAY=$(date +%Y-%m-%d)
echo "详情页链接: $FRONTEND_URL/summary/$TODAY"
echo "历史页链接: $FRONTEND_URL"
echo ""
echo "请确保前端服务正在运行:"
echo "  cd ../frontend && npm run dev"
echo ""

# 显示验证清单
echo "📋 步骤 7: 验证清单"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "请检查以下内容:"
echo "  □ 邮件头部有 '📖 查看完整详情' 按钮"
echo "  □ 邮件底部有 '🌐 在线查看完整报告' 按钮"
echo "  □ 邮件底部有 '📚 浏览历史日报' 链接"
echo "  □ 点击链接能正确跳转"
echo "  □ 详情页显示完整内容"
echo "  □ 首页显示历史列表"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     演示完成！                                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 相关文档:"
echo "  - EMAIL_FEATURE_SUMMARY.md       功能总结"
echo "  - EMAIL_DETAIL_LINK_GUIDE.md     使用指南"
echo "  - QUICK_REFERENCE_EMAIL_LINKS.md 快速参考"
echo ""
