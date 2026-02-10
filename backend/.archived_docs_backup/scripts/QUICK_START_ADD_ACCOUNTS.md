# 添加 Twitter 账号 - 完整指南

## 📋 当前状态

由于 Twitter API 限制，无法自动获取账号的 user_id：
- ❌ twitterapi.io API 无法获取用户信息
- ❌ 官方 Twitter API 免费额度已用完（CreditsDepleted）
- ❌ 网页抓取受到反爬虫限制

**解决方案**：手动获取 user_id 后批量导入

---

## 🚀 快速开始（3 步完成）

### 步骤 1: 获取 User IDs

访问 **https://tweeterid.com/**

逐个输入以下 username（不带 @）：

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

### 步骤 2: 编辑导入文件

打开文件：`scripts/user_ids_to_import.txt`

添加账号信息（格式：`username user_id`）：

```
swyx 33521530
gregisenberg 1234567890
joshwoodward 9876543210
...
```

### 步骤 3: 运行导入脚本

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python scripts/import_user_ids.py
```

或使用快速导入脚本：

```bash
./scripts/quick_import.sh
```

---

## 📝 详细说明

### 什么是 User ID？

User ID 是 Twitter 账号的唯一数字标识符，例如：
- `elonmusk` 的 user_id 是 `44196397`
- `karpathy` 的 user_id 是 `1270166613`

### 为什么需要 User ID？

Twitter API 使用 user_id 而不是 username 来获取推文，因为：
- Username 可以更改，但 user_id 永远不变
- API 调用需要 user_id 作为参数

### 如何获取 User ID？

**方法 1: 使用在线工具（推荐）**

1. 访问 https://tweeterid.com/
2. 输入 username（例如：`swyx`）
3. 点击 "Get User ID"
4. 复制显示的数字

**方法 2: 使用浏览器开发者工具**

1. 访问 `https://twitter.com/username`
2. 按 F12 打开开发者工具
3. 切换到 "Network" 标签
4. 刷新页面
5. 搜索 "UserByScreenName"
6. 在响应中查找 `"rest_id"` 字段

**方法 3: 使用其他在线工具**

- https://www.tweetbinder.com/blog/twitter-id/
- https://codeofaninja.com/tools/find-twitter-id/

---

## 📂 文件说明

### `scripts/usernames_to_add.txt`
包含需要添加的所有 username（已创建）

### `scripts/user_ids_to_import.txt`
导入文件，格式：`username user_id`（需要你编辑）

### `scripts/import_user_ids.py`
导入脚本，读取上面的文件并批量添加账号

### `scripts/quick_import.sh`
快速导入脚本，带确认提示

### `scripts/HOW_TO_ADD_ACCOUNTS.md`
完整的添加账号指南

---

## 💡 使用示例

### 示例 1: 添加单个账号

```bash
# 1. 获取 user_id
# 访问 https://tweeterid.com/
# 输入: swyx
# 得到: 33521530

# 2. 编辑文件
echo "swyx 33521530" >> scripts/user_ids_to_import.txt

# 3. 运行导入
./venv/bin/python scripts/import_user_ids.py
```

### 示例 2: 批量添加多个账号

```bash
# 1. 创建导入文件
cat > scripts/user_ids_to_import.txt << 'EOF'
swyx 33521530
karpathy 1270166613
elonmusk 44196397
EOF

# 2. 运行导入
./venv/bin/python scripts/import_user_ids.py
```

### 示例 3: 使用快速导入脚本

```bash
# 1. 编辑 scripts/user_ids_to_import.txt
# 添加账号信息

# 2. 运行快速导入
./scripts/quick_import.sh

# 脚本会显示将要导入的账号并要求确认
```

---

## ✅ 验证结果

### 查看当前监控的账号

```bash
python scripts/check_status.py
```

### 查看所有账号列表

```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

### 手动收集推文

```bash
python scripts/manual_collect.py
```

---

## 🔧 故障排除

### 问题 1: API 服务器未运行

**错误信息**：`❌ 错误: API 服务器未运行!`

**解决方法**：
```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 问题 2: 文件格式错误

**错误信息**：`第 X 行格式错误，已跳过`

**解决方法**：
确保文件格式正确：
- 每行一个账号
- Username 和 user_id 之间用空格分隔
- User_id 必须是纯数字
- 不要有多余的空格或特殊字符

正确格式：
```
swyx 33521530
karpathy 1270166613
```

错误格式：
```
swyx,33521530          # 不要用逗号
swyx  33521530         # 不要有多个空格
@swyx 33521530         # 不要加 @
swyx "33521530"        # 不要加引号
```

### 问题 3: 账号已存在

**信息**：`⊘ 已存在 @username`

**说明**：这不是错误，表示账号已经在监控列表中，会自动跳过。

### 问题 4: 找不到某个账号的 user_id

**可能原因**：
- Username 拼写错误
- 账号已被删除或暂停
- 账号已更改 username

**解决方法**：
1. 访问 `https://twitter.com/username` 确认账号是否存在
2. 检查 username 拼写（注意大小写）
3. 如果账号已更改 username，使用新的 username

---

## 📊 当前需要添加的账号

共 28 个账号：

| # | Username | 说明 |
|---|----------|------|
| 1 | swyx | |
| 2 | gregisenberg | |
| 3 | joshwoodward | |
| 4 | kevinweil | |
| 5 | petergyang | |
| 6 | thenanyu | |
| 7 | realmadhuguru | |
| 8 | mckaywrigley | |
| 9 | stevenbjohnson | |
| 10 | amandaaskell | |
| 11 | _catwu | |
| 12 | trq212 | |
| 13 | GoogleLabs | |
| 14 | george__mack | |
| 15 | raizamrtn | |
| 16 | amasad | |
| 17 | rauchg | |
| 18 | rileybrown | |
| 19 | alexalbert__ | |
| 20 | hamelhusain | |
| 21 | levie | |
| 22 | garrytan | |
| 23 | lulumeservey | |
| 24 | venturetwins | |
| 25 | attturck | |
| 26 | joulee | |
| 27 | PJaccetturo | |
| 28 | zarazhangrui | |

---

## 🎯 下一步

添加完账号后：

1. **查看状态**
   ```bash
   python scripts/check_status.py
   ```

2. **手动收集推文**（可选，不等待定时任务）
   ```bash
   python scripts/manual_collect.py
   ```

3. **等待自动收集**
   - 系统每 2 小时自动收集推文
   - 每天上午 8:00（北京时间）发送邮件摘要

4. **查看 API 文档**
   访问：http://localhost:8000/docs

---

## 📞 需要帮助？

如果遇到问题：

1. 查看日志：`tail -f /tmp/backend.log`
2. 检查系统状态：`python scripts/check_status.py`
3. 查看 API 健康状态：`curl http://localhost:8000/api/health`
4. 查看系统指标：`curl http://localhost:8000/api/metrics`

---

## 🔄 自动化建议

如果你经常需要添加账号，建议：

1. **申请 Twitter Developer 账号**
   - 访问：https://developer.twitter.com/
   - 申请更高的 API 配额
   - 这样就可以自动获取 user_id

2. **使用付费 Twitter API 服务**
   - 考虑升级 Twitter API 计划
   - 或使用第三方 API 服务

3. **批量处理**
   - 一次性获取所有需要的 user_id
   - 保存到文件中以备后用
   - 定期更新账号列表

---

## 📝 总结

由于 API 限制，当前需要手动获取 user_id。虽然多了一步，但这是最可靠的方法：

✅ **优点**：
- 100% 成功率
- 不受 API 限制
- 可以批量处理
- 一次设置，长期使用

⏱️ **时间估算**：
- 单个账号：约 30 秒
- 28 个账号：约 15-20 分钟

🎯 **推荐流程**：
1. 打开 https://tweeterid.com/
2. 打开 `scripts/user_ids_to_import.txt`
3. 逐个查询并记录
4. 运行导入脚本
5. 完成！
