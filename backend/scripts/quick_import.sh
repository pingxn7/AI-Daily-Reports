#!/bin/bash
# 快速添加账号的辅助脚本

echo "=================================="
echo "Twitter 账号批量添加工具"
echo "=================================="
echo ""
echo "步骤 1: 获取 User IDs"
echo "  访问: https://tweeterid.com/"
echo "  输入 username，获取 user_id"
echo ""
echo "步骤 2: 编辑导入文件"
echo "  文件: scripts/user_ids_to_import.txt"
echo "  格式: username user_id"
echo ""
echo "步骤 3: 运行导入"
echo "  ./scripts/quick_import.sh"
echo ""
echo "=================================="
echo ""

# 检查文件是否存在
if [ ! -f "scripts/user_ids_to_import.txt" ]; then
    echo "❌ 错误: 找不到 scripts/user_ids_to_import.txt"
    echo ""
    echo "请创建该文件并添加账号信息"
    echo "格式: username user_id"
    exit 1
fi

# 检查文件是否为空或只有注释
if ! grep -v '^#' scripts/user_ids_to_import.txt | grep -v '^[[:space:]]*$' > /dev/null; then
    echo "❌ 错误: user_ids_to_import.txt 文件为空"
    echo ""
    echo "请添加账号信息，格式:"
    echo "  username user_id"
    echo ""
    echo "示例:"
    echo "  swyx 33521530"
    echo "  karpathy 1270166613"
    exit 1
fi

# 显示将要导入的账号
echo "将要导入的账号:"
echo "----------------------------------"
grep -v '^#' scripts/user_ids_to_import.txt | grep -v '^[[:space:]]*$'
echo "----------------------------------"
echo ""

# 询问确认
read -p "确认导入这些账号? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 运行导入脚本
echo ""
./venv/bin/python scripts/import_user_ids.py
