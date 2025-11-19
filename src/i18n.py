"""
国际化 (i18n) 模块
支持中英文切换
"""

TRANSLATIONS = {
    # 语言选择
    "language": {
        "en": "Language",
        "zh": "语言"
    },

    # 页面标题和描述
    "page_title": {
        "en": "UGC Creator Settlement System",
        "zh": "UGC结算管理系统"
    },
    "page_subtitle": {
        "en": "Automatically fetch video data from Notion, scrape view counts, and calculate settlements",
        "zh": "自动从Notion读取视频数据，爬取播放量，并计算结算金额"
    },
    "version": {
        "en": "Version: 1.3 - Currency ($) and View Rounding (2025-11-18)",
        "zh": "版本: 1.3 - 货币单位($)和播放量向下取整 (2025-11-18)"
    },

    # 侧边栏 - 配置
    "config": {
        "en": "Configuration",
        "zh": "配置"
    },
    "notion_token": {
        "en": "Notion Token",
        "zh": "Notion Token"
    },
    "notion_token_help": {
        "en": "Format: ntn_xxxxxxxxxxxxx",
        "zh": "格式: ntn_xxxxxxxxxxxxx"
    },
    "master_db_id": {
        "en": "Master Database ID",
        "zh": "主数据库ID"
    },
    "master_db_id_help": {
        "en": "Get from Notion database URL, 32 characters (without hyphens)",
        "zh": "从Notion数据库URL中获取，32位字符（不含连字符）"
    },
    "config_complete": {
        "en": "✅ Configuration Complete",
        "zh": "✅ 配置完成"
    },
    "config_incomplete": {
        "en": "⚠️ Please enter Notion Token and Database ID",
        "zh": "⚠️ 请输入Notion Token和数据库ID"
    },

    # 爬取设置
    "scrape_settings": {
        "en": "Scraping Settings",
        "zh": "爬取设置"
    },
    "scrape_delay": {
        "en": "Scraping Delay (seconds)",
        "zh": "爬取延迟（秒）"
    },
    "scrape_delay_help": {
        "en": "Delay between each scrape to avoid being blocked",
        "zh": "每次爬取之间的延迟，避免被封禁"
    },

    # 使用说明
    "usage_guide": {
        "en": "Usage Guide",
        "zh": "使用说明"
    },

    # Tab 标题
    "tab_update_views": {
        "en": "🔄 Update Notion Views",
        "zh": "🔄 更新Notion Views"
    },
    "tab_settlement": {
        "en": "💰 Settlement Calculation",
        "zh": "💰 结算计算"
    },
    "tab_records": {
        "en": "📊 Settlement Records",
        "zh": "📊 结算记录"
    },
    "tab_system_info": {
        "en": "ℹ️ System Information",
        "zh": "ℹ️ 系统信息"
    },

    # 更新Views页面
    "update_views_header": {
        "en": "🔄 Update Notion Views",
        "zh": "🔄 更新Notion Views"
    },
    "update_views_description": {
        "en": "Automatically scrape view counts from Instagram and TikTok, and update to Notion",
        "zh": "自动从Instagram和TikTok爬取播放量，并更新到Notion"
    },
    "master_db": {
        "en": "Master Database ID",
        "zh": "主数据库ID"
    },
    "delay": {
        "en": "Delay",
        "zh": "延迟"
    },
    "start_batch_update": {
        "en": "🚀 Start Batch Update",
        "zh": "🚀 开始批量更新"
    },
    "detailed_logs": {
        "en": "📋 Detailed Logs",
        "zh": "📋 详细日志"
    },

    # 统计信息
    "update_stats": {
        "en": "📊 Update Statistics",
        "zh": "📊 更新统计"
    },
    "creators_processed": {
        "en": "Creators Processed",
        "zh": "处理创作者"
    },
    "tables_found": {
        "en": "Tables Found",
        "zh": "找到表格"
    },
    "videos_updated": {
        "en": "Videos Updated",
        "zh": "更新视频"
    },
    "total_views": {
        "en": "Total Views",
        "zh": "总播放量"
    },

    # 创作者详情
    "creator_details": {
        "en": "👥 Creator Details & Settlement Preview",
        "zh": "👥 创作者详情与结算预览"
    },
    "video_count": {
        "en": "Video Count",
        "zh": "视频数"
    },
    "label": {
        "en": "Label",
        "zh": "标签"
    },
    "not_set": {
        "en": "Not Set",
        "zh": "未设置"
    },
    "base_pay": {
        "en": "Base Pay",
        "zh": "底薪"
    },
    "commission": {
        "en": "Commission",
        "zh": "提成"
    },
    "settlement_amount": {
        "en": "Settlement Amount",
        "zh": "结算金额"
    },

    # 错误信息
    "errors_occurred": {
        "en": "⚠️ {count} error(s) occurred",
        "zh": "⚠️ 发生 {count} 个错误"
    },
    "view_error_details": {
        "en": "View Error Details",
        "zh": "查看错误详情"
    },

    # 状态信息
    "initializing": {
        "en": "Initializing...",
        "zh": "正在初始化..."
    },
    "batch_updating": {
        "en": "Batch updating all creators...",
        "zh": "正在批量更新所有创作者..."
    },
    "update_complete": {
        "en": "✅ Update Complete!",
        "zh": "✅ 更新完成！"
    },
    "update_failed": {
        "en": "❌ Update Failed",
        "zh": "❌ 更新失败"
    },
    "error": {
        "en": "Error",
        "zh": "错误"
    },
    "error_details": {
        "en": "Error Details",
        "zh": "错误详情"
    },

    # 结算页面
    "settlement_header": {
        "en": "💰 Settlement Calculation",
        "zh": "💰 结算计算"
    },
    "settlement_description": {
        "en": "Calculate monthly settlement amounts for creators",
        "zh": "按月计算创作者的结算金额"
    },
    "year": {
        "en": "Year",
        "zh": "年份"
    },
    "month": {
        "en": "Month",
        "zh": "月份"
    },
    "calculate_settlement": {
        "en": "📊 Calculate Settlement",
        "zh": "📊 计算结算"
    },
    "settlement_details": {
        "en": "📋 Settlement Details for {year}-{month}",
        "zh": "📋 {year}年{month}月结算明细"
    },
    "total_creators": {
        "en": "Total Creators",
        "zh": "总创作者"
    },
    "total_videos": {
        "en": "Total Videos",
        "zh": "总视频"
    },
    "total_settlement": {
        "en": "Total Settlement",
        "zh": "总结算"
    },
    "download_csv": {
        "en": "📥 Download CSV",
        "zh": "📥 下载CSV"
    },
    "no_records": {
        "en": "ℹ️ No settlement records for {year}-{month}",
        "zh": "ℹ️ 暂无{year}年{month}月的结算记录"
    },

    # 结算记录页面
    "records_header": {
        "en": "📊 Settlement Records",
        "zh": "📊 结算记录"
    },
    "records_description": {
        "en": "View historical settlement records",
        "zh": "查看历史结算记录"
    },
    "no_records_found": {
        "en": "ℹ️ No settlement records found",
        "zh": "ℹ️ 暂无结算记录"
    },
    "download": {
        "en": "📥 Download",
        "zh": "📥 下载"
    },

    # 系统信息页面
    "system_info_header": {
        "en": "ℹ️ System Information",
        "zh": "ℹ️ 系统信息"
    },
    "version_info": {
        "en": "📦 Version Information",
        "zh": "📦 版本信息"
    },
    "features": {
        "en": "✨ Features",
        "zh": "✨ 功能特点"
    },
    "settlement_rules": {
        "en": "💰 Settlement Rules",
        "zh": "💰 结算规则"
    },
    "tech_stack": {
        "en": "🛠️ Tech Stack",
        "zh": "🛠️ 技术栈"
    },
    "data_directory": {
        "en": "📁 Data Directory",
        "zh": "📁 数据目录"
    },
    "recent_update_logs": {
        "en": "📋 Recent Update Logs",
        "zh": "📋 最近更新日志"
    },
    "no_update_logs": {
        "en": "No update logs",
        "zh": "暂无更新日志"
    },

    # 表格列名
    "creator": {
        "en": "Creator",
        "zh": "创作者"
    },
    "ugc_type": {
        "en": "UGC Type",
        "zh": "UGC类型"
    },
    "total": {
        "en": "Total",
        "zh": "总计"
    },

    # 结算状态
    "fetching_data": {
        "en": "Fetching data...",
        "zh": "正在获取数据..."
    },
    "processing_data": {
        "en": "Processing data...",
        "zh": "正在处理数据..."
    },
    "calculating_settlement": {
        "en": "Calculating settlement...",
        "zh": "正在计算结算..."
    },
    "saving_records": {
        "en": "Saving settlement records...",
        "zh": "正在保存结算记录..."
    },
    "calculation_complete": {
        "en": "✅ Settlement Calculation Complete!",
        "zh": "✅ 结算计算完成！"
    },
    "calculation_failed": {
        "en": "❌ Calculation Failed",
        "zh": "❌ 计算失败"
    },
    "calculation_success": {
        "en": "Successfully calculated settlement for {year}-{month}, total {count} creator(s)",
        "zh": "成功计算{year}年{month}月的结算，共{count}位创作者"
    },

    # 配置错误
    "config_error": {
        "en": "❌ Please configure Notion Token and Database ID in the sidebar first",
        "zh": "❌ 请先在左侧配置Notion Token和数据库ID"
    },
}


def get_text(key: str, lang: str = "zh", **kwargs) -> str:
    """
    获取翻译文本

    Args:
        key: 文本键名
        lang: 语言代码 ('en' 或 'zh')
        **kwargs: 格式化参数

    Returns:
        翻译后的文本
    """
    if key not in TRANSLATIONS:
        return f"[Missing: {key}]"

    text = TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get("zh", key))

    # 格式化文本（如果有参数）
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text


# 语言选项
LANGUAGE_OPTIONS = {
    "en": "🇺🇸 English",
    "zh": "🇨🇳 中文"
}


def translate_ugc_type(ugc_type: str, lang: str = "zh") -> str:
    """
    翻译 UGC 类型显示文本

    Args:
        ugc_type: UGC类型（英文版，如 "Core UGC ($20/video)"）
        lang: 目标语言

    Returns:
        翻译后的 UGC 类型
    """
    if lang == "zh":
        # 将 /video 替换为 /条
        return ugc_type.replace("/video", "/条")
    return ugc_type
