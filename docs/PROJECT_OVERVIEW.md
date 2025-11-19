# UGC结算管理系统 - 项目概览

## 📋 项目简介

这是一个完整的UGC视频结算管理系统，能够自动从Notion数据库读取视频数据，爬取Instagram和TikTok的播放量，并自动更新到Notion，最后计算结算金额。

## 🎯 核心功能

### 1. 自动更新Notion播放量（最高优先级）
- ✅ 批量从主数据库获取所有创作者
- ✅ 自动查找每个创作者页面内的子表格
- ✅ 智能检测字段（支持不同命名方式）
- ✅ 从Instagram和TikTok爬取播放量
- ✅ 自动合并跨平台views
- ✅ 更新Views字段到Notion

### 2. 结算计算
- ✅ 按月计算底薪和提成
- ✅ 自动区分大UGC和小UGC
- ✅ 生成结算报表
- ✅ 保存和查看历史记录

### 3. 数据管理
- ✅ 数据存储和导出
- ✅ 更新日志记录
- ✅ 详细调试信息

## 🏗️ 技术架构

### 核心模块

1. **notion_integration.py** - Notion API集成
   - `NotionIntegration` 类: 处理所有Notion操作
   - `format_database_id()`: 格式化数据库ID
   - 支持：
     - 查询数据库
     - 获取页面子块
     - 查找子数据库
     - 自动检测字段
     - 批量更新

2. **view_scraper.py** - 播放量爬取
   - `ViewScraper` 类: 爬取Instagram和TikTok播放量
   - 支持：
     - 自动识别平台
     - 多种爬取策略
     - 数字格式解析（K/M/B/万等）
     - 防封禁延迟

3. **utils.py** - 工具函数
   - `SettlementCalculator` 类: 结算计算器
   - `DataStorage` 类: 数据存储管理
   - 工具函数: 格式化、日期解析等

4. **app.py** - Streamlit Web应用
   - 用户界面
   - 配置管理
   - 进度显示
   - 结果展示

### 技术栈

- **Python 3.13+**
- **Streamlit**: Web界面框架
- **notion-client**: Notion API官方客户端
- **requests + BeautifulSoup**: HTTP请求和HTML解析
- **pandas**: 数据处理和分析

## 📊 数据流程

```
1. Notion主数据库
   ↓
2. 获取所有创作者页面
   ↓
3. 查找每个创作者的子表格
   ↓
4. 检测字段（Link, Views等）
   ↓
5. 获取所有视频行
   ↓
6. 爬取播放量
   ├── Instagram
   └── TikTok
   ↓
7. 合并跨平台views
   ↓
8. 更新Notion Views字段
   ↓
9. 生成统计报告
```

## 🔧 关键技术细节

### Notion API调用

使用新版本notion-client的`request()`方法：
```python
response = client.request(
    path=f"databases/{database_id}/query",
    method="POST",
    body={}
)
```

### 字段自动检测

系统会自动检测所有：
- **URL类型字段**: Link, Link1, Link2, link等（排除Views字段）
- **Number类型字段**: Views, View, views等

不需要手动统一字段名称。

### 播放量爬取策略

支持多种爬取方法：
1. Meta标签（og:description）
2. JSON-LD结构化数据
3. 页面JSON数据
4. 页面文本搜索

### 防封禁机制

- 可配置的请求延迟
- 随机User-Agent
- Session保持
- 错误重试

## 📁 项目结构

```
babymiluxclaude/
├── app.py                   # Streamlit主应用 (15KB)
├── notion_integration.py    # Notion API集成 (17KB)
├── view_scraper.py         # 播放量爬取 (11KB)
├── utils.py                # 工具函数 (9KB)
├── requirements.txt        # Python依赖
├── README.md              # 项目说明
├── QUICKSTART.md          # 快速开始指南
├── PROJECT_OVERVIEW.md    # 项目概览（本文件）
├── test_system.py         # 系统测试脚本
├── start.sh               # Linux/macOS启动脚本
├── start.bat              # Windows启动脚本
├── .gitignore            # Git忽略文件
└── data/                 # 数据目录（自动创建）
    ├── settlement_*.csv  # 结算记录
    ├── config.json       # 配置文件
    └── update_log.jsonl  # 更新日志
```

## 🔐 安全注意事项

1. **Notion Token安全**
   - Token具有完整的数据库访问权限
   - 不要提交到Git仓库
   - 不要分享给他人
   - 在.gitignore中已排除

2. **爬取限制**
   - 遵守平台的反爬虫政策
   - 设置合理的延迟
   - 不要频繁爬取

3. **数据隐私**
   - 所有数据存储在本地
   - 不上传到第三方服务
   - CSV导出注意保密

## 🚀 部署建议

### 本地使用（推荐）
```bash
./start.sh  # 或 start.bat
```

### 服务器部署
1. 克隆代码到服务器
2. 安装依赖：`pip install -r requirements.txt`
3. 配置环境变量
4. 运行：`streamlit run app.py --server.port 8501`

### Docker部署（可选）
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 🔄 工作流程建议

### 日常使用
1. **每周更新播放量**
   - 运行应用
   - 点击"批量更新所有创作者"
   - 等待完成，查看日志

2. **月初计算结算**
   - 选择上个月的年月
   - 点击"计算结算"
   - 导出CSV发送给创作者

3. **定期备份数据**
   - 备份`data/`目录
   - 导出重要的结算记录

### 故障排查
1. 查看详细日志
2. 检查Notion连接
3. 测试单个创作者
4. 调整爬取延迟
5. 查看错误信息

## 📈 性能指标

### 处理能力
- 创作者数量: 无限制（建议<100）
- 视频数量: 无限制（建议<1000）
- 爬取速度: ~2-5秒/视频（取决于延迟设置）

### 预计耗时
- 10个创作者，50个视频: ~2-5分钟
- 20个创作者，100个视频: ~5-10分钟

### 资源占用
- 内存: ~100-200MB
- CPU: 低
- 网络: 中等

## 🛠️ 扩展开发

### 添加新平台支持
在`view_scraper.py`中添加：
```python
def scrape_youtube_views(self, url: str) -> Optional[int]:
    # 实现YouTube爬取逻辑
    pass
```

### 自定义结算规则
在`utils.py`的`SettlementCalculator`中修改：
```python
self.base_pay_large = 20  # 修改大UGC底薪
self.commission_rate = 1  # 修改提成比例
```

### 添加新功能
1. 在相应模块中添加函数
2. 在`app.py`中添加UI界面
3. 测试功能
4. 更新文档

## 📝 版本历史

### v1.0.0 (2025-01-17)
- ✅ 初始版本发布
- ✅ 核心功能实现
- ✅ Notion Views自动更新
- ✅ 结算计算功能
- ✅ 完整文档

## 🎓 学习资源

- [Notion API 文档](https://developers.notion.com/)
- [Streamlit 文档](https://docs.streamlit.io/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas 文档](https://pandas.pydata.org/docs/)

## 📞 支持和反馈

如需帮助：
1. 查看QUICKSTART.md快速开始指南
2. 查看README.md常见问题
3. 运行test_system.py检查系统状态
4. 查看详细日志了解错误原因

## 🙏 致谢

感谢所有开源项目的贡献者：
- Notion API团队
- Streamlit团队
- 所有Python开源库的维护者

---

**祝使用愉快！如有问题欢迎反馈。** 🎉
