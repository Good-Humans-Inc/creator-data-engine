# 快速开始指南

## 📋 前置要求

- Python 3.13 或更高版本
- Notion账户和集成Token
- 主数据库的访问权限

## 🚀 安装步骤

### 方法1: 使用启动脚本（推荐）

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

脚本会自动：
1. 创建虚拟环境
2. 安装所有依赖
3. 启动应用

### 方法2: 手动安装

1. **创建虚拟环境**
```bash
python3 -m venv venv
```

2. **激活虚拟环境**

macOS/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行应用**
```bash
streamlit run app.py
```

## 🔑 配置Notion集成

### 1. 创建Notion集成

1. 访问 https://www.notion.so/my-integrations
2. 点击 "+ New integration"
3. 填写信息：
   - Name: `UGC结算系统`
   - Associated workspace: 选择你的工作区
   - Capabilities: 勾选 "Read content", "Update content"
4. 点击 "Submit"
5. 复制 **Internal Integration Token**（格式：`ntn_xxxxxxxxxxxxx`）

### 2. 连接到数据库

1. 打开你的Notion主数据库页面
2. 点击右上角 "..." (更多选项)
3. 选择 "Connections"
4. 搜索并添加你刚创建的集成 "UGC结算系统"

### 3. 获取数据库ID

从数据库URL中获取：
```
https://www.notion.so/[workspace]/[DATABASE_ID]?v=...
```

DATABASE_ID 是一个32位字符的ID（可能包含连字符，系统会自动处理）

例如：`2af95b547d5e811b8b01e1b61f64f900`

## 📊 使用系统

### 1. 配置

打开应用后，在左侧边栏输入：
- **Notion Token**: 你的集成Token
- **主数据库ID**: 你的数据库ID

### 2. 更新播放量

1. 切换到 "🔄 更新Notion Views" 标签页
2. 调整爬取延迟（建议2-5秒，避免被封禁）
3. 点击 "🚀 开始批量更新"
4. 等待更新完成，查看统计信息

### 3. 计算结算

1. 切换到 "💰 结算计算" 标签页
2. 选择年份和月份
3. 点击 "📊 计算结算"
4. 查看结算明细，可下载CSV

### 4. 查看记录

在 "📊 结算记录" 标签页可以查看所有历史结算记录

## 📝 数据结构要求

### 主数据库
- 包含所有创作者的信息
- 每个创作者是一个页面（card）
- 建议字段：Creator (Title), Label, Platform(s), Email

### 子表格（在创作者页面内）
- **Name字段** (Title类型): 视频名称，如 "20251114"
- **Link字段** (URL类型): Instagram或TikTok链接
- **Link2字段** (URL类型, 可选): 第二个平台的链接
- **Views字段** (Number类型): 播放量（系统自动填充）

**注意**: 字段名称可以有所不同，系统会自动检测：
- URL字段: Link, Link1, Link2, link, link1, link2 等
- Views字段: Views, View, views, view 等

## ⚠️ 注意事项

1. **首次使用建议**
   - 先测试单个创作者，确认无误后再批量更新
   - 设置较长的爬取延迟（3-5秒）

2. **爬取限制**
   - Instagram和TikTok都有反爬虫机制
   - 不要频繁爬取，建议每天或每周更新一次
   - 如遇到爬取失败，可能需要增加延迟

3. **权限问题**
   - 确保Notion集成已连接到主数据库
   - 子表格会自动继承父页面的connection权限

4. **数据安全**
   - 不要分享你的Notion Token
   - Token具有完整的数据库访问权限

## 🐛 常见问题

### Q: 找不到子表格？
A:
- 检查创作者页面是否真的有子表格
- 确保Notion集成已连接到主数据库
- 查看详细日志了解具体原因

### Q: 爬取失败？
A:
- 检查URL是否正确
- 增加爬取延迟（避免被封禁）
- 查看详细日志了解错误信息
- 某些私密视频可能无法爬取

### Q: 字段名称不统一？
A:
- 系统会自动检测所有URL和Number类型字段
- 不需要手动统一命名
- 查看详细日志确认系统检测到了哪些字段

### Q: 更新很慢？
A:
- 这是正常的，因为需要逐个爬取视频
- 爬取延迟设置得越长，耗时越久
- 建议在非工作时间运行批量更新

## 📞 获取帮助

如有问题：
1. 查看详细日志（在"更新Notion Views"页面展开"详细日志"）
2. 查看系统信息页面了解更多细节
3. 检查README.md中的技术文档

## 🎯 下一步

完成基础配置后，你可以：
1. 定期更新播放量（建议每周一次）
2. 每月计算结算金额
3. 导出结算记录给创作者
4. 根据需要调整结算规则（在utils.py中修改）

祝使用愉快！🎉
