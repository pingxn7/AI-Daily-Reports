# 📋 添加 Twitter 账号 - 快速参考

## 🚨 当前状况

由于 Twitter API 限制，无法自动获取 user_id：
- ❌ twitterapi.io API 不可用
- ❌ 官方 Twitter API 免费额度已用完
- ❌ 网页抓取受限

**解决方案**：手动获取 user_id 后批量导入

---

## ⚡ 三种添加方法

### 方法 1: 批量导入（推荐，适合多个账号）

```bash
# 1. 编辑文件
nano scripts/user_ids_to_import.txt

# 2. 添加账号（格式: username user_id）
swyx 33521530
karpathy 1270166613

# 3. 运行导入
./venv/bin/python scripts/import_user_ids.py
```

### 方法 2: 交互式添加（适合少量账号）

```bash
# 运行交互式工具
./venv/bin/python scripts/add_accounts_interactive.py

# 按提示逐个输入 username 和 user_id
```

### 方法 3: 快速导入脚本

```bash
# 1. 编辑文件
nano scripts/user_ids_to_import.txt

# 2. 运行快速导入（带确认）
./scripts/quick_import.sh
```

---

## 🔍 如何获取 User ID

### 最简单的方法：使用 tweeterid.com

1. 访问：**https://tweeterid.com/**
2. 输入 username（例如：`swyx`）
3. 点击 "Get User ID"
4. 复制数字 ID

### 其他在线工具

- https://www.tweetbinder.com/blog/twitter-id/
- https://codeofaninja.com/tools/find-twitter-id/

---

## 📝 需要添加的 28 个账号

```
swyx
gregisenberg
joshwoodward
kevinweil
petergyang
thenanyu
realmadhuguru
mckaywrigley
stevenbjohnson
amandaaskell
_catwu
trq212
GoogleLabs
george__mack
raizamrtn
amasad
rauchg
rileybrown
alexalbert__
hamelhusain
levie
garrytan
lulumeservey
venturetwins
attturck
joulee
PJaccetturo
zarazhangrui
```

---

## 📂 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/usernames_to_add.txt` | 需要添加的 username 列表 |
| `scripts/user_ids_to_import.txt` | 导入文件（需要编辑） |
| `scripts/import_user_ids.py` | 批量导入脚本 |
| `scripts/add_accounts_interactive.py` | 交互式添加工具 |
| `scripts/quick_import.sh` | 快速导入脚本 |
| `scripts/QUICK_START_ADD_ACCOUNTS.md` | 完整指南 |
| `scripts/HOW_TO_ADD_ACCOUNTS.md` | 详细说明 |

---

## ✅ 验证和下一步

### 查看当前账号

```bash
python scripts/check_status.py
```

### 手动收集推文

```bash
python scripts/manual_collect.py
```

### 查看 API 状态

```bash
curl http://localhost:8000/api/metrics | python3 -m json.tool
```

---

## 💡 快速示例

### 添加单个账号

```bash
# 1. 获取 user_id
# 访问 https://tweeterid.com/
# 输入: swyx → 得到: 33521530

# 2. 添加到文件
echo "swyx 33521530" >> scripts/user_ids_to_import.txt

# 3. 导入
./venv/bin/python scripts/import_user_ids.py
```

### 批量添加多个账号

```bash
# 1. 创建导入文件
cat > scripts/user_ids_to_import.txt << 'EOF'
swyx 33521530
karpathy 1270166613
elonmusk 44196397
EOF

# 2. 导入
./venv/bin/python scripts/import_user_ids.py
```

---

## 🎯 推荐工作流程

1. **打开两个窗口**
   - 窗口 1: https://tweeterid.com/
   - 窗口 2: `nano scripts/user_ids_to_import.txt`

2. **逐个查询并记录**
   - 在 tweeterid.com 输入 username
   - 复制 user_id
   - 粘贴到文件中（格式：`username user_id`）

3. **批量导入**
   ```bash
   ./venv/bin/python scripts/import_user_ids.py
   ```

4. **验证结果**
   ```bash
   python scripts/check_status.py
   ```

---

## ⏱️ 时间估算

- 单个账号：约 30 秒
- 28 个账号：约 15-20 分钟
- 批量导入：约 10 秒

---

## 🔧 常见问题

### Q: API 服务器未运行？

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Q: 文件格式错误？

确保格式正确：
```
username user_id
```

不要：
- 使用逗号分隔
- 添加 @ 符号
- 使用引号
- 有多余空格

### Q: 账号已存在？

这是正常的，系统会自动跳过已存在的账号。

---

## 📞 需要帮助？

查看完整指南：
```bash
cat scripts/QUICK_START_ADD_ACCOUNTS.md
cat scripts/HOW_TO_ADD_ACCOUNTS.md
```

查看系统日志：
```bash
tail -f /tmp/backend.log
```

---

## 🎉 完成后

添加完账号后，系统会：
- ✅ 每 2 小时自动收集推文
- ✅ 使用 AI 分析推文内容
- ✅ 每天上午 8:00（北京时间）发送邮件摘要
- ✅ 提供 Web API 查看数据

祝使用愉快！🚀
