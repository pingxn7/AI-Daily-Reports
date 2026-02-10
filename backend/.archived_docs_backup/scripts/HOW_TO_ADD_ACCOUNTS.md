# 如何批量添加 Twitter 账号

由于 Twitter API 的限制，需要手动获取账号的 user_id。以下是详细步骤：

## 方法 1: 使用在线工具（推荐）

### 步骤 1: 获取 User IDs

访问以下任一网站：
- **https://tweeterid.com/** （推荐，最简单）
- https://www.tweetbinder.com/blog/twitter-id/
- https://codeofaninja.com/tools/find-twitter-id/

在 tweeterid.com 上：
1. 输入 username（不带 @）
2. 点击 "Get User ID"
3. 复制显示的数字 ID

### 步骤 2: 创建导入文件

创建文件 `scripts/user_ids_to_import.txt`，格式如下：

```
username user_id
```

例如：
```
swyx 1234567890
karpathy 9876543210
elonmusk 44196397
```

### 步骤 3: 运行导入脚本

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python scripts/import_user_ids.py
```

## 方法 2: 使用浏览器开发者工具

### 步骤 1: 打开 Twitter 个人主页

访问 `https://twitter.com/username`

### 步骤 2: 打开开发者工具

- Chrome/Edge: 按 F12 或 Ctrl+Shift+I (Windows) / Cmd+Option+I (Mac)
- Firefox: 按 F12 或 Ctrl+Shift+I (Windows) / Cmd+Option+I (Mac)

### 步骤 3: 查找 User ID

1. 切换到 "Network" (网络) 标签
2. 刷新页面 (F5)
3. 在过滤器中搜索 "UserByScreenName"
4. 点击找到的请求
5. 在 "Response" (响应) 标签中查找 `"rest_id"` 字段
6. 复制该字段的值（这就是 user_id）

## 方法 3: 批量处理（适合大量账号）

### 使用 Python 脚本批量查询

如果你有很多账号需要添加，可以：

1. 将所有 username 保存到 `scripts/usernames_to_add.txt`（已创建）
2. 访问 https://tweeterid.com/
3. 逐个输入 username 并记录 user_id
4. 将结果保存到 `scripts/user_ids_to_import.txt`
5. 运行导入脚本

## 当前需要添加的账号列表

已为你创建了文件 `scripts/usernames_to_add.txt`，包含以下账号：

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

## 快速开始

1. 访问 https://tweeterid.com/
2. 逐个输入上面的 username
3. 将结果保存为以下格式到 `scripts/user_ids_to_import.txt`:
   ```
   swyx 1234567890
   gregisenberg 9876543210
   ...
   ```
4. 运行导入脚本:
   ```bash
   ./venv/bin/python scripts/import_user_ids.py
   ```

## 注意事项

- User ID 是一串数字，通常 10-19 位
- Username 不区分大小写，但建议使用正确的大小写
- 如果账号不存在或已被删除，tweeterid.com 会显示错误
- 导入脚本会自动跳过已存在的账号

## 故障排除

### 问题: tweeterid.com 无法访问

尝试其他工具：
- https://www.tweetbinder.com/blog/twitter-id/
- https://codeofaninja.com/tools/find-twitter-id/

### 问题: 找不到某个账号的 user_id

可能原因：
- Username 拼写错误
- 账号已被删除或暂停
- 账号已更改 username

解决方法：
- 访问 https://twitter.com/username 确认账号是否存在
- 检查 username 拼写
- 如果账号已更改 username，使用新的 username

### 问题: 导入脚本报错

确保：
1. API 服务器正在运行
2. 文件格式正确（username 和 user_id 之间用空格分隔）
3. User ID 是纯数字

## 示例：完整流程

```bash
# 1. 查看需要添加的账号
cat scripts/usernames_to_add.txt

# 2. 访问 https://tweeterid.com/ 获取 user_ids

# 3. 创建导入文件
cat > scripts/user_ids_to_import.txt << 'EOF'
swyx 33521530
karpathy 1270166613
EOF

# 4. 运行导入脚本
./venv/bin/python scripts/import_user_ids.py

# 5. 查看结果
python scripts/check_status.py
```

## 自动化建议

如果你经常需要添加账号，建议：
1. 申请 Twitter Developer 账号并获取更高的 API 配额
2. 或者使用付费的 Twitter API 服务
3. 这样就可以自动获取 user_id，无需手动查找
