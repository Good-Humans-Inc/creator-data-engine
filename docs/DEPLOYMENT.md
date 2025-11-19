# 🌐 部署指南 - 让系统在网页上运行

你有多种方式将系统部署到网页，无需每次通过终端启动。

---

## 🚀 方案1：Streamlit Cloud（推荐 - 完全免费）

**优点**：
- ✅ 完全免费
- ✅ 自动部署，推送代码即更新
- ✅ 提供公网访问地址
- ✅ 无需服务器维护

**步骤**：

### 1. 准备GitHub仓库
```bash
cd /Users/siyangli/Desktop/babymiluxclaude

# 初始化Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: UGC结算管理系统"

# 在GitHub创建仓库后，推送代码
git remote add origin https://github.com/你的用户名/ugc-settlement.git
git push -u origin main
```

### 2. 部署到Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的仓库：`ugc-settlement`
5. Main file path: `app.py`
6. 点击 "Deploy"

### 3. 配置密钥（重要！）

在Streamlit Cloud的App settings中：
1. 点击 "⚙️ Settings"
2. 选择 "Secrets"
3. 添加配置（可选，也可以在网页界面直接输入）：
```toml
[notion]
token = "your_notion_token_here"
master_db_id = "your_database_id_here"
```

### 4. 完成！

部署后你会得到一个公网地址，类似：
```
https://your-app-name.streamlit.app
```

在任何地方打开这个链接就能使用！

---

## 🖥️ 方案2：本地保持运行（无需每次启动终端）

### macOS/Linux - 使用后台服务

创建一个LaunchAgent（开机自启）：

**文件**: `~/Library/LaunchAgents/com.ugc.settlement.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ugc.settlement</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/siyangli/Desktop/babymiluxclaude/venv/bin/streamlit</string>
        <string>run</string>
        <string>/Users/siyangli/Desktop/babymiluxclaude/app.py</string>
        <string>--server.port</string>
        <string>8501</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ugc-settlement.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ugc-settlement-error.log</string>
</dict>
</plist>
```

**启动服务**：
```bash
launchctl load ~/Library/LaunchAgents/com.ugc.settlement.plist
```

然后访问：http://localhost:8501

### Windows - 使用任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：系统启动时
4. 操作：启动程序
   - 程序：`venv\Scripts\streamlit.exe`
   - 参数：`run app.py --server.port 8501`
   - 起始于：`C:\Users\...\babymiluxclaude`

访问：http://localhost:8501

---

## ☁️ 方案3：云服务器部署

### 3.1 使用Railway.app（推荐）

**优点**：
- 每月免费$5额度
- 自动从GitHub部署
- 提供HTTPS域名

**步骤**：
1. 访问 https://railway.app
2. 使用GitHub登录
3. "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. 添加环境变量（在Settings中）
6. 自动部署完成

### 3.2 使用Render.com（免费）

**步骤**：
1. 访问 https://render.com
2. "New" → "Web Service"
3. 连接GitHub仓库
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. 部署

### 3.3 使用Heroku

需要添加配置文件：

**Procfile**:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

部署：
```bash
heroku create your-app-name
git push heroku main
```

---

## 🏢 方案4：内网部署（团队共享）

如果只需要团队内部访问：

### 使用Docker（推荐）

创建 `Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY . .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  ugc-settlement:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**启动**：
```bash
docker-compose up -d
```

然后团队成员访问：`http://你的内网IP:8501`

---

## 🔒 安全配置建议

### 1. 添加身份验证

创建 `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 2. 使用环境变量

创建 `.streamlit/secrets.toml`:
```toml
[notion]
token = "ntn_xxxxxxxxxxxxx"
master_db_id = "2af95b547d5e811b8b01e1b61f64f900"
```

在代码中读取：
```python
import streamlit as st

# 优先使用secrets，如果没有则使用session_state
if "notion" in st.secrets:
    notion_token = st.secrets["notion"]["token"]
    master_db_id = st.secrets["notion"]["master_db_id"]
```

---

## 📊 部署方案对比

| 方案 | 费用 | 难度 | 适用场景 |
|------|------|------|----------|
| **Streamlit Cloud** | 免费 | ⭐ 最简单 | 个人使用，小团队 |
| **本地后台运行** | 免费 | ⭐⭐ 简单 | 个人电脑常开 |
| **Railway/Render** | 免费-$5/月 | ⭐⭐ 简单 | 小团队，需要稳定运行 |
| **Docker内网** | 免费（需服务器） | ⭐⭐⭐ 中等 | 公司内部使用 |
| **Heroku** | $7/月 | ⭐⭐⭐ 中等 | 需要稳定的商业服务 |

---

## 🎯 推荐方案

### 个人使用
→ **Streamlit Cloud**（完全免费，最简单）

### 小团队（3-10人）
→ **Streamlit Cloud** 或 **Railway.app**

### 公司内部（需要安全控制）
→ **Docker内网部署**

---

## 📝 快速部署到Streamlit Cloud

**最快5分钟完成部署！**

```bash
# 1. 创建GitHub仓库并推送代码
cd /Users/siyangli/Desktop/babymiluxclaude
git init
git add .
git commit -m "UGC结算管理系统"

# 2. 在GitHub创建仓库后
git remote add origin https://github.com/你的用户名/ugc-settlement.git
git push -u origin main

# 3. 访问 streamlit.io/cloud 部署
# 4. 完成！获得永久网址
```

---

## ❓ 常见问题

### Q: 部署后如何保护Notion Token？
A: 使用Streamlit的Secrets功能，Token不会暴露在代码中

### Q: 免费方案有限制吗？
A: Streamlit Cloud免费版有资源限制，但对于这个应用完全够用

### Q: 可以自定义域名吗？
A: Streamlit Cloud支持自定义域名（需要升级计划）

### Q: 如何更新代码？
A: 推送到GitHub后，Streamlit Cloud会自动重新部署

---

**选择适合你的方案，让系统随时随地可用！** 🚀
