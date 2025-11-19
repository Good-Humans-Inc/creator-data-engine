# UGC Creator Settlement System | UGC结算管理系统

<div align="center">

[🇺🇸 English](#english) | [🇨🇳 中文](#chinese)

**An automated UGC video settlement management system with Notion integration**
**一个自动化的UGC视频结算管理系统，集成Notion数据库**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io)

</div>

---

<a name="english"></a>

## 🇺🇸 English

### Overview

An automated UGC (User-Generated Content) settlement system that fetches video data from Notion databases, scrapes view counts from Instagram and TikTok, and automatically calculates settlement amounts with multi-language support (English/Chinese).

### ✨ Features

- ✅ **Automatic View Count Updates**: Batch scrape view counts from Instagram and TikTok
- ✅ **Smart Field Detection**: Automatically recognizes Link and Views fields with flexible naming
- ✅ **Batch Processing**: One-click update for all creators' video data
- ✅ **Settlement Calculation**: Automatic monthly base pay and commission calculation
- ✅ **Multi-language Support**: Switch between English and Chinese in-app
- ✅ **Detailed Logging**: Complete debugging information for troubleshooting
- ✅ **Multiple Videos Per Day**: Support for date formats like "20251114-1", "20251114-2"

### 🚀 Quick Start

#### One-Click Launch (Recommended)

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

#### Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Notion Integration**
   - Visit [Notion Integrations](https://www.notion.so/my-integrations)
   - Create a new integration and get your Token (format: `ntn_xxxxxxxxxxxxx`)
   - In your Notion master database page, click "..." → "Connections" → Add your integration

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

4. **Using the System**
   - Enter **Notion Token** and **Master Database ID** in the sidebar
   - Navigate to "Update Notion Views" tab
   - Click "Start Batch Update" button
   - Switch language using the dropdown at the top of the sidebar

### 📋 Data Structure Requirements

#### Master Database
- Contains all creator information
- Each creator is a page (card)
- Must have a "Label" property to distinguish between Core UGC and Discord UGC

#### Child Tables (Inside Creator Pages)
- **Name Field** (Title type): Video date, e.g., "20251114" or "20251114-1" (for multiple videos on the same day)
- **Link Field** (URL type): Instagram or TikTok link
- **Link2 Field** (URL type, optional): Second platform link
- **Views Field** (Number type): View count (auto-populated by system)

### 💰 Settlement Rules

#### Base Pay
- **Core UGC**: $20 per video
- **Discord UGC**: $10 per video

#### Commission
- $1 per 1000 views (rounded down)
- Cross-platform auto-merge: Views from the same video on different platforms are automatically combined

#### Settlement Period
- Monthly settlement (e.g., settle November videos on December 1st)
- Automatic grouping by video Name field date

### 🛠️ Tech Stack

- **Streamlit**: Web UI framework
- **notion-client**: Notion API integration
- **requests + BeautifulSoup**: View count scraping
- **Selenium**: Alternative scraper for dynamic content
- **pandas**: Data processing

### 📁 Project Structure

```
creator-data-engine/
├── app.py                    # Streamlit main application
├── requirements.txt          # Python dependencies
├── start.sh / start.bat      # Launch scripts
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
│
├── src/                      # Core source code
│   ├── i18n.py              # Internationalization (i18n)
│   ├── notion_integration.py # Notion API integration
│   ├── view_scraper.py       # View scraper (BeautifulSoup)
│   ├── view_scraper_selenium.py # View scraper (Selenium)
│   └── utils.py              # Utility functions
│
├── tests/                    # Test files
│   ├── test_date_parsing.py  # Date parsing tests
│   ├── test_settlement_logic.py # Settlement logic tests
│   └── ...                   # Other tests
│
├── docs/                     # Documentation
│   ├── QUICKSTART.md         # Quick start guide
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── PROJECT_OVERVIEW.md   # Project overview
│   └── SUMMARY.md            # Summary
│
├── scripts/                  # Utility scripts
│   └── debug_label.py        # Debugging tools
│
└── data/                     # Data directory (.gitignored)
    ├── settlement_YYYY_MM.csv # Settlement records
    └── update_log.jsonl      # Update logs
```

### ❓ FAQ

**Q: Why can't the system find child tables?**
A: Ensure:
1. Your Notion integration is connected to the master database
2. Child tables exist within creator pages
3. Child tables auto-inherit parent page connection permissions

**Q: What to do if scraping fails?**
A: The system will auto-retry. If it continues to fail:
1. Check if URLs are correct
2. Increase scraping delay (avoid anti-scraping measures)
3. Check detailed logs for error reasons

**Q: What if field names are inconsistent?**
A: The system auto-detects all URL-type fields (Link, Link1, Link2, etc.) - no manual unification needed

### ⚠️ Important Notes

- Set reasonable delays (2-5 seconds recommended) to avoid platform bans
- Test with a single creator first before batch updating
- Keep your Notion Token secure and never share it

### 📚 Documentation & Deployment

For detailed development and deployment instructions:
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)

### 📄 License

This project is licensed under the [MIT License](LICENSE).

### 🤝 Support

For questions or suggestions, please submit an Issue or Pull Request.

---

<a name="chinese"></a>

## 🇨🇳 中文

### 项目简介

一个自动化的UGC视频结算管理系统，能够从Notion数据库读取视频数据，爬取Instagram和TikTok播放量，并自动计算结算金额。支持中英文双语切换。

### ✨ 功能特点

- ✅ **自动更新Notion播放量**：批量从Instagram和TikTok爬取播放量
- ✅ **智能字段检测**：自动识别Link和Views字段，适配不同的命名方式
- ✅ **批量处理**：一键更新所有创作者的视频数据
- ✅ **结算计算**：按月自动计算底薪和提成
- ✅ **多语言支持**：应用内中英文自由切换
- ✅ **详细日志**：完整的调试信息帮助排查问题
- ✅ **同日多视频**：支持"20251114-1"、"20251114-2"等日期格式

### 🚀 快速开始

详细教程请查看 [QUICKSTART.md](docs/QUICKSTART.md)

#### 一键启动（推荐）

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

#### 手动启动

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置Notion集成**
   - 访问 [Notion Integrations](https://www.notion.so/my-integrations)
   - 创建新的集成，获取Token（格式：`ntn_xxxxxxxxxxxxx`）
   - 在Notion主数据库页面，点击右上角"..."→"Connections"→添加你的集成

3. **运行应用**
   ```bash
   streamlit run app.py
   ```

4. **使用系统**
   - 在左侧输入**Notion Token**和**主数据库ID**
   - 选择"更新Notion Views"页面
   - 点击"开始批量更新"按钮
   - 使用侧边栏顶部的下拉菜单切换语言

### 📋 数据结构要求

#### 主数据库
- 包含所有创作者信息
- 每个创作者是一个页面（card）
- 需要有"Label"属性用于区分大UGC(Core UGC)和小UGC(Discord UGC)

#### 子表格（在创作者页面内）
- **Name字段**（Title类型）：视频日期，如"20251114"或"20251114-1"（同一天多个视频）
- **Link字段**（URL类型）：Instagram或TikTok链接
- **Link2字段**（URL类型，可选）：第二个平台的链接
- **Views字段**（Number类型）：播放量（系统自动填充）

### 💰 结算规则

#### 底薪
- **大UGC (Core UGC)**：$20/条视频
- **小UGC (Discord UGC)**：$10/条视频

#### 提成
- 每1000 views = $1（向下取整）
- 跨平台自动合并：同一视频在不同平台的views会自动合并

#### 结算周期
- 按月结算（例如：12月1日结算11月的所有视频）
- 根据视频Name字段的日期自动分组

### 🛠️ 技术架构

- **Streamlit**：Web界面框架
- **notion-client**：Notion API集成
- **requests + BeautifulSoup**：播放量爬取
- **Selenium**：动态内容爬取备选方案
- **pandas**：数据处理

### 📁 文件结构

```
creator-data-engine/
├── app.py                    # Streamlit主应用
├── requirements.txt          # 依赖包列表
├── start.sh / start.bat      # 启动脚本
├── LICENSE                   # MIT开源协议
├── README.md                 # 项目说明
│
├── src/                      # 核心源代码
│   ├── i18n.py              # 国际化(i18n)
│   ├── notion_integration.py # Notion API集成
│   ├── view_scraper.py       # 播放量爬取（BeautifulSoup）
│   ├── view_scraper_selenium.py # 播放量爬取（Selenium）
│   └── utils.py              # 工具函数（结算计算、数据存储）
│
├── tests/                    # 测试文件
│   ├── test_date_parsing.py  # 日期解析测试
│   ├── test_settlement_logic.py # 结算逻辑测试
│   └── ...                   # 其他测试
│
├── docs/                     # 文档
│   ├── QUICKSTART.md         # 快速开始指南
│   ├── DEPLOYMENT.md         # 部署说明
│   ├── PROJECT_OVERVIEW.md   # 项目概览
│   └── SUMMARY.md            # 总结文档
│
├── scripts/                  # 辅助脚本
│   └── debug_label.py        # 调试工具
│
└── data/                     # 数据目录（.gitignore）
    ├── settlement_YYYY_MM.csv # 结算记录
    └── update_log.jsonl      # 更新日志
```

### ❓ 常见问题

**Q: 为什么找不到子表格？**
A: 确保：
1. 你的Notion集成已连接到主数据库
2. 创作者页面内确实有子表格
3. 子表格会自动继承父页面的connection权限

**Q: 爬取失败怎么办？**
A: 系统会自动重试，如果持续失败：
1. 检查URL是否正确
2. 适当增加爬取延迟（避免被反爬虫）
3. 查看详细日志了解错误原因

**Q: 字段名称不统一怎么办？**
A: 系统会自动检测所有URL类型字段（Link、Link1、Link2等），不需要手动统一命名

### ⚠️ 注意事项

- 爬取时请设置合理的延迟（建议2-5秒），避免被平台封禁
- 首次运行建议先测试单个创作者，确认无误后再批量更新
- 保管好你的Notion Token，不要泄露给他人

### 📚 开发与部署

详细的开发和部署说明请查看：
- [部署指南](docs/DEPLOYMENT.md)
- [项目概览](docs/PROJECT_OVERVIEW.md)

### 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

### 🤝 支持

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

<div align="center">

**Made with ❤️ for UGC Creators**

</div>
