import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    """读取二进制文件并转换为base64字符串"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path, target_url):
    """创建一个带链接的图片HTML"""
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code

def apply_custom_style():
    """应用自定义CSS样式"""
    
    # 路径配置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    bg_image_path = os.path.join(project_root, 'ui', 'background-light-05.png')
    
    # 如果背景图片存在，转换为base64
    bg_image_css = ""
    if os.path.exists(bg_image_path):
        bin_str = get_base64_of_bin_file(bg_image_path)
        # 注意：这里不使用缩进，避免 Markdown 代码块解析问题
        bg_image_css = f"""
.stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
"""

    custom_css = f"""
<style>
/* 全局字体和颜色优化 */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');

/* 定义动画 */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-6px); }}
    100% {{ transform: translateY(0px); }}
}}

@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

/* 流星特效动画 */
@keyframes tail {{
    0% {{ width: 0; }}
    30% {{ width: 100px; }}
    100% {{ width: 0; }}
}}

@keyframes shooting {{
    0% {{ transform: translateX(0) translateY(0) rotate(-45deg); opacity: 1; }}
    100% {{ transform: translateX(-300px) translateY(300px) rotate(-45deg); opacity: 0; }}
}}

@keyframes shining {{
    0% {{ width: 0; }}
    50% {{ width: 30px; }}
    100% {{ width: 0; }}
}}

.stApp {{
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #5A6185;
}}

/* 移除顶部白边和Header */
header[data-testid="stHeader"] {{
    background: transparent;
}}

/* 主容器入场动画 */
.main .block-container {{
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

/* 标题样式 - 使用衬线字体和深紫色 */
h1 {{
    font-family: 'Cormorant Garamond', serif;
    font-weight: 500;
    color: #5A6185;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
    font-size: 3rem !important;
}}

h2, h3 {{
    font-family: 'Cormorant Garamond', serif;
    color: #5A6185;
    font-weight: 500;
    letter-spacing: 0.5px;
}}

/* 自动为标题添加爱心装饰 */
h1::before, h2::before {{
    content: "♡";
    font-size: 80%;
    color: #5A6185;
    margin-right: 10px;
    font-family: 'Cormorant Garamond', serif;
    font-weight: normal;
    vertical-align: middle;
}}

/* 移除底部footer */
footer {{
    display: none;
}}

/* 应用背景图片 */
{bg_image_css}

/* 侧边栏高级美化 */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.6);
    box-shadow: 4px 0 15px rgba(0,0,0,0.03);
}}

[data-testid="stSidebarUserContent"] {{
    padding-top: 1rem;
}}

/* 按钮高级美化 */
.stButton > button {{
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(0,0,0,0.05);
    padding: 0.6rem 1.2rem;
    letter-spacing: 0.3px;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    border-color: transparent;
}}

.stButton > button:active {{
    transform: translateY(0);
}}

/* Primary按钮特殊样式 - 深紫色 + 微光特效 */
.stButton > button[kind="primary"] {{
    background: linear-gradient(90deg, #5A6185 0%, #7279a0 50%, #5A6185 100%);
    background-size: 200% 100%;
    border: none;
    box-shadow: 0 4px 15px rgba(90, 97, 133, 0.2);
    color: white;
    font-family: 'Inter', sans-serif;
    letter-spacing: 1px;
    animation: shimmer 3s infinite linear;
}}

.stButton > button[kind="primary"]:hover {{
    background-position: 100% 0;
    box-shadow: 0 8px 25px rgba(90, 97, 133, 0.3);
    transition: all 0.4s ease;
}}

/* 进度条美化 - 深紫色 */
.stProgress > div > div > div > div {{
    background: #5A6185;
    border-radius: 10px;
    height: 8px;
}}

/* Tab 高级美化 */
.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
    padding: 0.5rem 0;
    border-bottom: none;
}}

.stTabs [data-baseweb="tab"] {{
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 20px;
    padding: 8px 20px;
    border: 1px solid rgba(90, 97, 133, 0.2);
    font-weight: 400;
    transition: all 0.2s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    color: #5A6185;
    font-family: 'Inter', sans-serif;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background-color: rgba(255, 255, 255, 0.8);
    transform: translateY(-1px);
    color: #4a5175;
}}

.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: #5A6185;
    color: white;
    border: none;
    box-shadow: 0 4px 12px rgba(90, 97, 133, 0.25);
}}

/* Metric Value 颜色 */
[data-testid="stMetricValue"] {{
    font-size: 1.8rem;
    font-weight: 600;
    color: #5A6185;
    font-family: 'Cormorant Garamond', serif;
}}

/* Metric卡片玻璃拟态效果 + 悬浮动画 */
[data-testid="stMetric"] {{
    background-color: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.6);
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    transition: all 0.3s ease;
    animation: float 6s ease-in-out infinite;
}}

div[data-testid="column"]:nth-of-type(1) [data-testid="stMetric"] {{ animation-delay: 0s; }}
div[data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] {{ animation-delay: 1s; }}
div[data-testid="column"]:nth-of-type(3) [data-testid="stMetric"] {{ animation-delay: 2s; }}
div[data-testid="column"]:nth-of-type(4) [data-testid="stMetric"] {{ animation-delay: 3s; }}

[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    background-color: rgba(255, 255, 255, 0.8);
}}

/* 数据表格玻璃拟态 */
[data-testid="stDataFrame"] {{
    background-color: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}}

/* Alert/Info 框美化 */
.stAlert {{
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}}

/* 输入控件美化 */
.stTextInput > div > div > input,
.stSelectbox > div > div > div {{
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within {{
    background-color: #fff;
    box-shadow: 0 4px 15px rgba(90, 97, 133, 0.1);
    border-color: #5A6185;
}}

/* 流星特效容器 */
.shooting-stars {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}}

.star {{
    position: absolute;
    top: 50%;
    left: 50%;
    height: 2px;
    background: linear-gradient(-45deg, #FFD700, rgba(255, 215, 0, 0));
    filter: drop-shadow(0 0 8px #FFA500);
    animation: tail 3000ms ease-in-out infinite, shooting 3000ms ease-in-out infinite;
    opacity: 0;
}}

.star::before {{
    content: '';
    position: absolute;
    top: calc(50% - 1px);
    right: 0;
    height: 2px;
    background: linear-gradient(-45deg, rgba(255, 215, 0, 0), #FFD700, rgba(255, 215, 0, 0));
    transform: translateX(50%) rotateZ(45deg);
    border-radius: 100%;
    animation: shining 3000ms ease-in-out infinite;
}}

.star::after {{
    content: '';
    position: absolute;
    top: calc(50% - 1px);
    right: 0;
    height: 2px;
    background: linear-gradient(-45deg, rgba(255, 215, 0, 0), #FFD700, rgba(255, 215, 0, 0));
    transform: translateX(50%) rotateZ(45deg);
    border-radius: 100%;
    animation: shining 3000ms ease-in-out infinite;
}}

.star:nth-child(1) {{
    top: 0;
    left: 50%;
    animation-delay: 2s;
}}

.star:nth-child(2) {{
    top: 20%;
    left: 80%;
    animation-delay: 4s;
}}

.star:nth-child(3) {{
    top: 10%;
    left: 30%;
    animation-delay: 6s;
}}
</style>
"""

    shooting_star_layer = """
<div class="shooting-stars">
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
</div>
"""

    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(shooting_star_layer, unsafe_allow_html=True)

def display_sidebar_logo():
    """在侧边栏显示Logo"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logo_path = os.path.join(project_root, 'ui', 'Rectangle.png')
    
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
        st.sidebar.markdown("---")
