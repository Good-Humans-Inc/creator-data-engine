@echo off
REM UGC结算管理系统启动脚本 (Windows)

echo 🎬 UGC结算管理系统
echo ==================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.13+
    pause
    exit /b 1
)

echo ✓ Python已安装

REM 检查是否已安装依赖
if not exist "venv" (
    echo.
    echo 📦 首次运行，正在创建虚拟环境...
    python -m venv venv

    echo 📦 激活虚拟环境...
    call venv\Scripts\activate.bat

    echo 📦 安装依赖包...
    pip install -r requirements.txt
) else (
    echo ✓ 虚拟环境已存在
    call venv\Scripts\activate.bat
)

echo.
echo 🚀 启动Streamlit应用...
echo.

streamlit run app.py

pause
