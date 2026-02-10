# 🚀 快速开始 - Twitter 账号监听系统

## ✅ 系统状态

```
✅ 监听账号：17 个
✅ 已收集推文：15 条
✅ 系统运行：正常
✅ 下次收集：2026-02-08 12:00
```

## 🎯 立即行动（3 步完成）

### 步骤 1: 获取 User ID

访问 **https://tweeterid.com/**，获取以下 3 个最重要账号的 user_id：

1. **geoffreyhinton** - Geoffrey Hinton（图灵奖得主）
2. **Yoshua_Bengio** - Yoshua Bengio（图灵奖得主）
3. **aidangomez** - Aidan Gomez（Cohere CEO）

### 步骤 2: 添加账号

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/add_accounts_interactive.py
```

按照提示输入 user_id 即可。

### 步骤 3: 验证

```bash
./scripts/check_status.sh
```

## 📋 常用命令

```bash
# 查看系统状态
./scripts/check_status.sh

# 查看账号列表
python scripts/add_accounts_interactive.py --list

# 添加账号
python scripts/add_accounts_interactive.py

# 查看 API 文档
open http://localhost:8000/docs
```

## 📚 详细文档

- **README.md** - 完整说明
- **ACTION_LIST.md** - 行动清单
- **COMPLETE_GUIDE.md** - 详细指南

---

**下一步**：访问 https://tweeterid.com/ 获取 user_id，然后运行交互式工具添加账号。
