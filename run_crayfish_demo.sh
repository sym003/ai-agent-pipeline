#!/bin/bash
# 小龙虾赛马模块安装和运行脚本

set -e

echo "🦐 小龙虾养殖赛马模块 - 安装和演示脚本"
echo "======================================="

# 检查是否在正确目录
if [[ ! -f "src/crayfish_racing/models.py" ]]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [[ ! -d "venv" ]]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "🔧 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "🔧 安装依赖包..."
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    # 最小依赖安装
    pip install pydantic fastapi uvicorn
fi

# 创建examples目录（如果不存在）
mkdir -p examples

# 运行演示
echo "🏃 运行小龙虾赛马演示..."
python examples/crayfish_racing_demo.py

echo "✅ 演示完成！"
echo ""
echo "💡 下一步你可以:"
echo "  1. 查看 src/crayfish_racing/ 目录了解完整实现"
echo "  2. 修改 examples/crayfish_racing_demo.py 中的示例数据"
echo "  3. 集成到你的FastAPI应用中使用API接口"