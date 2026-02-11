#!/bin/bash

# Vercel + Render 部署快速检查脚本

echo "🔍 AI News Collector - 部署前检查"
echo "=================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查必需的工具
echo "📋 检查必需工具..."
echo ""

# Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓ Git 已安装${NC}"
else
    echo -e "${RED}✗ Git 未安装${NC}"
    echo "  安装: brew install git"
fi

# Node.js
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js 已安装 ($(node -v))${NC}"
else
    echo -e "${RED}✗ Node.js 未安装${NC}"
    echo "  安装: brew install node"
fi

# Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python 已安装 ($(python3 --version))${NC}"
else
    echo -e "${RED}✗ Python 未安装${NC}"
fi

# AWS CLI
if command -v aws &> /dev/null; then
    echo -e "${GREEN}✓ AWS CLI 已安装${NC}"
else
    echo -e "${YELLOW}⚠ AWS CLI 未安装（配置 S3 时需要）${NC}"
    echo "  安装: brew install awscli"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查项目文件
echo "📁 检查项目文件..."
echo ""

if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓ backend/requirements.txt 存在${NC}"
else
    echo -e "${RED}✗ backend/requirements.txt 不存在${NC}"
fi

if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓ frontend/package.json 存在${NC}"
else
    echo -e "${RED}✗ frontend/package.json 不存在${NC}"
fi

if [ -f "backend/app/main.py" ]; then
    echo -e "${GREEN}✓ backend/app/main.py 存在${NC}"
else
    echo -e "${RED}✗ backend/app/main.py 不存在${NC}"
fi

if [ -f "frontend/app/page.tsx" ]; then
    echo -e "${GREEN}✓ frontend/app/page.tsx 存在${NC}"
else
    echo -e "${RED}✗ frontend/app/page.tsx 不存在${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Git 状态
echo "🔄 检查 Git 状态..."
echo ""

if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"

    # 检查是否有远程仓库
    if git remote -v | grep -q "origin"; then
        echo -e "${GREEN}✓ 远程仓库已配置${NC}"
        git remote -v | head -2
    else
        echo -e "${YELLOW}⚠ 未配置远程仓库${NC}"
        echo "  需要创建 GitHub 仓库并关联"
    fi
else
    echo -e "${YELLOW}⚠ Git 仓库未初始化${NC}"
    echo "  运行: git init"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# API Keys 检查清单
echo "🔑 API Keys 准备清单"
echo ""
echo "请确认你已经准备好以下 API Keys："
echo ""
echo "  [ ] Twitter API Key (https://twitterapi.io)"
echo "  [ ] Anthropic API Key (https://console.anthropic.com)"
echo "  [ ] AWS Access Key & Secret (https://console.aws.amazon.com)"
echo "  [ ] Resend API Key (https://resend.com)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 账号检查清单
echo "👤 账号准备清单"
echo ""
echo "请确认你已经注册以下服务："
echo ""
echo "  [ ] GitHub 账号 (https://github.com)"
echo "  [ ] Vercel 账号 (https://vercel.com)"
echo "  [ ] Render 账号 (https://render.com)"
echo "  [ ] AWS 账号 (https://aws.amazon.com)"
echo "  [ ] Resend 账号 (https://resend.com)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 下一步提示
echo "📝 下一步操作"
echo ""
echo "1. 如果所有检查都通过，可以开始部署"
echo "2. 打开部署指南："
echo "   open DEPLOY_VERCEL_RENDER.md"
echo ""
echo "3. 或者查看快速开始："
echo "   cat DEPLOY_VERCEL_RENDER.md | head -100"
echo ""
echo "4. 按照指南的 10 个步骤依次操作"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示："
echo "  - 整个部署过程约需 60-90 分钟"
echo "  - 建议先完整阅读一遍指南"
echo "  - 准备好所有 API Keys 再开始"
echo "  - 遇到问题查看指南的故障排查章节"
echo ""
echo "🎉 祝部署顺利！"
echo ""
