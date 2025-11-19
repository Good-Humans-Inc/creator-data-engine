"""
UGC结算管理系统 - Streamlit主应用
自动从Notion读取视频数据，爬取播放量，并计算结算金额
"""

import streamlit as st
import sys

# 强制重新加载utils模块，确保使用最新代码
if 'src.utils' in sys.modules:
    import importlib
    from src import utils
    importlib.reload(utils)

from src.notion_integration import NotionIntegration, format_database_id
from src.view_scraper_selenium import ViewScraperSelenium
from src.utils import SettlementCalculator, DataStorage, format_number
from src.i18n import get_text, LANGUAGE_OPTIONS, translate_ugc_type
import pandas as pd
from datetime import datetime
import traceback


# 页面配置
st.set_page_config(
    page_title="UGC结算管理系统",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # 默认中文
if 'notion_token' not in st.session_state:
    st.session_state.notion_token = ''
if 'master_db_id' not in st.session_state:
    st.session_state.master_db_id = ''
if 'debug_logs' not in st.session_state:
    st.session_state.debug_logs = []


def main():
    """主函数"""

    # 获取当前语言
    lang = st.session_state.language

    # 侧边栏 - 语言选择和配置
    with st.sidebar:
        # 语言选择器（放在最顶部）
        st.subheader("🌐 " + get_text("language", lang))
        selected_lang = st.selectbox(
            label="Select Language / 选择语言",
            options=list(LANGUAGE_OPTIONS.keys()),
            format_func=lambda x: LANGUAGE_OPTIONS[x],
            index=0 if lang == "en" else 1,
            key="language_selector",
            label_visibility="collapsed"
        )

        # 如果语言改变，更新session_state并刷新
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

        st.divider()

        # 配置
        st.header("⚙️ " + get_text("config", lang))

        # Notion Token
        notion_token = st.text_input(
            get_text("notion_token", lang),
            type="password",
            value=st.session_state.notion_token,
            help=get_text("notion_token_help", lang)
        )
        if notion_token:
            st.session_state.notion_token = notion_token

        # 主数据库ID
        master_db_id = st.text_input(
            get_text("master_db_id", lang),
            value=st.session_state.master_db_id,
            help=get_text("master_db_id_help", lang)
        )
        if master_db_id:
            st.session_state.master_db_id = master_db_id

        # 连接状态
        if notion_token and master_db_id:
            st.success(get_text("config_complete", lang))
        else:
            st.warning(get_text("config_incomplete", lang))

        st.divider()

        # 爬取设置
        st.subheader(get_text("scrape_settings", lang))
        scrape_delay = st.slider(
            get_text("scrape_delay", lang),
            min_value=1.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
            help=get_text("scrape_delay_help", lang)
        )

        st.divider()

        # 使用说明（简化版，保留中文，避免复杂翻译）
        with st.expander("📖 " + get_text("usage_guide", lang)):
            if lang == "zh":
                st.markdown("""
                ### 快速开始
                1. 输入Notion Token和主数据库ID
                2. 选择"更新Notion Views"页面
                3. 点击"批量更新所有创作者"
                4. 等待更新完成

                ### 结算规则
                - **大UGC**: $20/条 + 提成
                - **小UGC**: $10/条 + 提成
                - **提成**: 每1000 views = $1 (向下取整)
                - **跨平台**: 自动合并同一视频的views
                """)
            else:
                st.markdown("""
                ### Quick Start
                1. Enter Notion Token and Master Database ID
                2. Go to "Update Notion Views" tab
                3. Click "Start Batch Update"
                4. Wait for completion

                ### Settlement Rules
                - **Core UGC**: $20/video + commission
                - **Discord UGC**: $10/video + commission
                - **Commission**: $1 per 1000 views (rounded down)
                - **Cross-platform**: Auto-merge views
                """)

    # 页面标题
    st.title("🎬 " + get_text("page_title", lang))
    st.markdown(get_text("page_subtitle", lang))
    st.caption(get_text("version", lang))

    # 主页面 - 标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("tab_update_views", lang),
        get_text("tab_settlement", lang),
        get_text("tab_records", lang),
        get_text("tab_system_info", lang)
    ])

    # Tab 1: 更新Notion Views
    with tab1:
        show_update_views_page(scrape_delay, lang)

    # Tab 2: 结算计算
    with tab2:
        show_settlement_page(lang)

    # Tab 3: 结算记录
    with tab3:
        show_records_page(lang)

    # Tab 4: 系统信息
    with tab4:
        show_system_info_page(lang)


def show_update_views_page(scrape_delay: float, lang: str = "zh"):
    """显示更新Views页面"""

    st.header(get_text("update_views_header", lang))
    st.markdown(get_text("update_views_description", lang))

    # 检查配置
    if not st.session_state.notion_token or not st.session_state.master_db_id:
        st.error(get_text("config_error", lang))
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        db_text = get_text("master_db", lang) if lang == "en" else "主数据库ID"
        delay_text = get_text("delay", lang) if lang == "en" else "爬取延迟"
        st.info(f"📊 {db_text}: `{st.session_state.master_db_id}`")
        st.info(f"⏱️ {delay_text}: {scrape_delay}" + ("s" if lang == "en" else "秒"))

    with col2:
        # 开始更新按钮
        if st.button(get_text("start_batch_update", lang), type="primary", use_container_width=True):
            start_batch_update(scrape_delay, lang)

    st.divider()

    # 显示更新日志
    if st.session_state.debug_logs:
        with st.expander(get_text("detailed_logs", lang), expanded=False):
            for log in st.session_state.debug_logs:
                st.text(log)


def start_batch_update(scrape_delay: float, lang: str = "zh"):
    """开始批量更新"""

    # 清空之前的日志
    st.session_state.debug_logs = []

    # 创建进度显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    stats_container = st.container()

    try:
        # 初始化
        status_text.text(get_text("initializing", lang))
        notion = NotionIntegration(st.session_state.notion_token)
        scraper = ViewScraperSelenium(delay=scrape_delay, headless=True)

        # 开始批量更新
        status_text.text(get_text("batch_updating", lang))
        stats = notion.batch_update_all_creators(
            master_db_id=st.session_state.master_db_id,
            scraper=scraper,
            delay=scrape_delay
        )

        # 关闭浏览器
        scraper.close()

        # 保存日志
        st.session_state.debug_logs = notion.debug_info

        # 更新进度条
        progress_bar.progress(100)
        status_text.text(get_text("update_complete", lang))

        # 显示统计信息
        with stats_container:
            st.success("### " + get_text("update_stats", lang))

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(get_text("creators_processed", lang), f"{stats['creators_processed']}")

            with col2:
                st.metric(get_text("tables_found", lang), f"{stats['tables_found']}")

            with col3:
                st.metric(get_text("videos_updated", lang), f"{stats['videos_updated']}")

            with col4:
                st.metric(get_text("total_views", lang), format_number(stats['total_views']))

            # 显示创作者详情和结算预览
            if stats.get('creator_details'):
                st.divider()
                st.subheader(get_text("creator_details", lang))

                calculator = SettlementCalculator()

                for creator in stats['creator_details']:
                    if creator['videos_updated'] > 0:
                        # 计算结算
                        settlement = calculator.calculate_settlement(
                            video_count=creator['videos_updated'],
                            total_views=creator['total_views'],
                            label=creator['label']
                        )

                        with st.expander(f"📋 {creator['name']} ({translate_ugc_type(settlement['ugc_type'], lang)})"):
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric(get_text("video_count", lang), creator['videos_updated'])
                            with col_b:
                                st.metric(get_text("total_views", lang), format_number(creator['total_views']))
                            with col_c:
                                st.metric(get_text("settlement_amount", lang), f"${settlement['total']:.2f}")

                            label_text = get_text("label", lang)
                            not_set_text = get_text("not_set", lang)
                            base_pay_text = get_text("base_pay", lang)
                            commission_text = get_text("commission", lang)
                            st.markdown(f"""
                            - **{label_text}**: {creator['label'] if creator['label'] else not_set_text}
                            - **{base_pay_text}**: ${settlement['base_pay']:.2f}
                            - **{commission_text}**: ${settlement['commission']:.2f}
                            """)

            # 显示错误
            if stats['errors']:
                st.warning(get_text("errors_occurred", lang, count=len(stats['errors'])))
                with st.expander(get_text("view_error_details", lang)):
                    for error in stats['errors']:
                        st.error(error)

        # 保存更新日志
        storage = DataStorage()
        storage.save_update_log({
            'timestamp': datetime.now().isoformat(),
            'action': 'batch_update',
            'details': stats
        })

    except Exception as e:
        # 确保关闭浏览器
        try:
            scraper.close()
        except:
            pass

        progress_bar.progress(0)
        status_text.text("❌ 更新失败")
        st.error(f"错误: {str(e)}")
        with st.expander("错误详情"):
            st.code(traceback.format_exc())


def show_settlement_page(lang: str = "zh"):
    """显示结算计算页面"""

    st.header(get_text("settlement_header", lang))
    st.markdown(get_text("settlement_description", lang))

    # 检查配置
    if not st.session_state.notion_token or not st.session_state.master_db_id:
        st.error(get_text("config_error", lang))
        return

    # 选择年月
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        current_year = datetime.now().year
        year = st.selectbox(
            get_text("year", lang),
            options=list(range(current_year - 2, current_year + 1)),
            index=2
        )

    with col2:
        current_month = datetime.now().month
        month = st.selectbox(
            get_text("month", lang),
            options=list(range(1, 13)),
            index=current_month - 1
        )

    with col3:
        if st.button(get_text("calculate_settlement", lang), type="primary", use_container_width=True):
            calculate_settlement(year, month, lang)

    st.divider()

    # 显示结算明细
    storage = DataStorage()
    settlement_df = storage.load_settlement_record(year, month)

    if settlement_df is not None:
        st.success("### 📋 " + get_text("settlement_details", lang, year=year, month=month))

        # 显示汇总
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(get_text("total_creators", lang), len(settlement_df))

        with col2:
            st.metric(get_text("total_videos", lang), int(settlement_df['video_count'].sum()))

        with col3:
            st.metric(get_text("total_views", lang), format_number(settlement_df['total_views'].sum()))

        with col4:
            st.metric(get_text("total_settlement", lang), f"${settlement_df['total'].sum():.2f}")

        # 显示明细表格
        st.dataframe(
            settlement_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "creator": get_text("creator", lang),
                "label": get_text("label", lang),
                "ugc_type": get_text("ugc_type", lang),
                "video_count": st.column_config.NumberColumn(get_text("video_count", lang), format="%d"),
                "total_views": st.column_config.NumberColumn(get_text("total_views", lang), format="%d"),
                "base_pay": st.column_config.NumberColumn(get_text("base_pay", lang), format="$%.2f"),
                "commission": st.column_config.NumberColumn(get_text("commission", lang), format="$%.2f"),
                "total": st.column_config.NumberColumn(get_text("total", lang), format="$%.2f"),
            }
        )

        # 下载按钮
        csv = settlement_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=get_text("download_csv", lang),
            data=csv,
            file_name=f"settlement_{year}_{month:02d}.csv",
            mime="text/csv"
        )

    else:
        st.info(get_text("no_records", lang, year=year, month=month))


def calculate_settlement(year: int, month: int, lang: str = "zh"):
    """计算结算"""

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text(get_text("fetching_data", lang))

        # 初始化
        notion = NotionIntegration(st.session_state.notion_token)
        calculator = SettlementCalculator()
        storage = DataStorage()

        # 获取所有创作者
        progress_bar.progress(20)
        creators = notion.get_all_creators(st.session_state.master_db_id)

        # 收集数据
        progress_bar.progress(40)
        status_text.text(get_text("processing_data", lang))

        creators_data = []
        for creator in creators:
            creator_id = creator['id']
            creator_name = creator['name']
            creator_label = creator.get('label', '')  # 从Notion获取Label字段

            # 查找子数据库
            child_dbs = notion.find_child_databases(creator_id)

            videos = []
            for child_db in child_dbs:
                # 检测字段
                link_fields, views_field = notion.detect_fields(child_db['id'])

                if not views_field:
                    continue

                # 获取视频行
                video_rows = notion.get_video_rows(child_db['id'], link_fields, views_field)

                for video in video_rows:
                    videos.append({
                        'date': video['name'],  # 假设Name是日期格式
                        'views': video['current_views']
                    })

            creators_data.append({
                'name': creator_name,
                'label': creator_label,  # 使用从Notion获取的Label
                'videos': videos
            })

        # 计算结算
        progress_bar.progress(60)
        status_text.text(get_text("calculating_settlement", lang))

        settlement_df = calculator.calculate_monthly_settlement(creators_data, year, month)

        # 保存结算记录
        progress_bar.progress(80)
        status_text.text(get_text("saving_records", lang))

        storage.save_settlement_record(settlement_df, year, month)

        # 完成
        progress_bar.progress(100)
        status_text.text(get_text("calculation_complete", lang))

        st.success(get_text("calculation_success", lang, year=year, month=month, count=len(settlement_df)))

        # 刷新页面
        st.rerun()

    except Exception as e:
        progress_bar.progress(0)
        status_text.text(get_text("calculation_failed", lang))
        st.error(get_text("error", lang) + ": " + str(e))
        with st.expander(get_text("error_details", lang)):
            st.code(traceback.format_exc())


def show_records_page(lang: str = "zh"):
    """显示结算记录页面"""

    st.header(get_text("records_header", lang))
    st.markdown(get_text("records_description", lang))

    storage = DataStorage()
    records = storage.list_settlement_records()

    if not records:
        st.info(get_text("no_records_found", lang))
        return

    # 显示记录列表
    for record in records:
        year = record['year']
        month = record['month']

        expander_title = f"📅 {year}-{month:02d}" if lang == "en" else f"📅 {year}年{month}月结算"
        with st.expander(expander_title):
            df = storage.load_settlement_record(year, month)

            if df is not None:
                # 汇总信息
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(get_text("creator", lang), len(df))

                with col2:
                    st.metric(get_text("video_count", lang), int(df['video_count'].sum()))

                with col3:
                    st.metric(get_text("total_views", lang), format_number(df['total_views'].sum()))

                with col4:
                    st.metric(get_text("total_settlement", lang), f"${df['total'].sum():.2f}")

                # 明细表格
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                # 下载按钮
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=get_text("download", lang),
                    data=csv,
                    file_name=f"settlement_{year}_{month:02d}.csv",
                    mime="text/csv",
                    key=f"download_{year}_{month}"
                )


def show_system_info_page(lang: str = "zh"):
    """显示系统信息页面"""

    st.header(get_text("system_info_header", lang))

    # 版本信息
    st.subheader(get_text("version_info", lang))
    st.info(get_text("page_title", lang) + " v1.3.0")

    # 功能说明
    st.subheader(get_text("features", lang))
    if lang == "zh":
        st.markdown("""
        - ✅ **自动更新播放量**: 批量从Instagram和TikTok爬取播放量
        - ✅ **智能字段检测**: 自动识别Link和Views字段
        - ✅ **批量处理**: 一键更新所有创作者的视频数据
        - ✅ **结算计算**: 按月自动计算底薪和提成
        - ✅ **详细日志**: 完整的调试信息
        """)
    else:
        st.markdown("""
        - ✅ **Automatic View Updates**: Batch scrape from Instagram and TikTok
        - ✅ **Smart Field Detection**: Auto-recognize Link and Views fields
        - ✅ **Batch Processing**: One-click update for all creators
        - ✅ **Settlement Calculation**: Auto-calculate monthly base pay and commission
        - ✅ **Detailed Logs**: Complete debugging information
        """)

    # 结算规则
    st.subheader(get_text("settlement_rules", lang))
    col1, col2 = st.columns(2)

    with col1:
        base_pay_title = "**Base Pay**" if lang == "en" else "**底薪**"
        st.markdown(base_pay_title)
        if lang == "zh":
            st.markdown("- 大UGC: $20/条")
            st.markdown("- 小UGC: $10/条")
        else:
            st.markdown("- Core UGC: $20/video")
            st.markdown("- Discord UGC: $10/video")

    with col2:
        commission_title = "**Commission**" if lang == "en" else "**提成**"
        st.markdown(commission_title)
        if lang == "zh":
            st.markdown("- 每1000 views = $1 (向下取整)")
            st.markdown("- 跨平台自动合并")
        else:
            st.markdown("- $1 per 1000 views (rounded down)")
            st.markdown("- Auto-merge cross-platform")

    # 技术栈
    st.subheader(get_text("tech_stack", lang))
    if lang == "zh":
        st.markdown("""
        - **Streamlit**: Web界面框架
        - **notion-client**: Notion API集成
        - **requests + BeautifulSoup**: 播放量爬取
        - **pandas**: 数据处理
        """)
    else:
        st.markdown("""
        - **Streamlit**: Web UI framework
        - **notion-client**: Notion API integration
        - **requests + BeautifulSoup**: View count scraping
        - **pandas**: Data processing
        """)

    # 数据目录
    st.subheader(get_text("data_directory", lang))
    storage = DataStorage()
    st.code(storage.data_dir)

    # 更新日志
    st.subheader(get_text("recent_update_logs", lang))
    logs = storage.load_update_logs(limit=10)

    if logs:
        for log in reversed(logs):
            timestamp = log.get('timestamp', '')
            action = log.get('action', '')
            details = log.get('details', {})

            with st.expander(f"{timestamp} - {action}"):
                st.json(details)
    else:
        st.info(get_text("no_update_logs", lang))


if __name__ == "__main__":
    main()
