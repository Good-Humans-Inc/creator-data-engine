#!/bin/bash
# UGC结算管理系统启动脚本

echo "🎬 UGC结算管理系统"
echo "=================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.13+"
    exit 1
fi

echo "✓ Python已安装: $(python3 --version)"

# 检查是否已安装依赖
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 首次运行，正在创建虚拟环境..."
    python3 -m venv venv

    echo "📦 激活虚拟环境..."
    source venv/bin/activate

    echo "📦 安装依赖包..."
    pip install -r requirements.txt
else
    echo "✓ 虚拟环境已存在"
    source venv/bin/activate
fi

echo ""
echo "🚀 启动Streamlit应用..."
echo ""

streamlit run app.py
