#!/bin/bash

# 重庆AI供需对接平台 - 启动脚本

echo "========================================="
echo "  重庆人工智能供需对接平台 MVP"
echo "========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: Node.js 未安装"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 后端设置
echo "📦 设置后端服务..."
cd backend

if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "安装Python依赖..."
pip install -q -r requirements.txt

if [ ! -f "ai_platform.db" ]; then
    echo "初始化数据库..."
    python init_db.py
fi

echo "启动后端服务..."
python -m app.main &
BACKEND_PID=$!
echo "后端服务 PID: $BACKEND_PID"

cd ..

# 等待后端启动
sleep 3

# 前端设置
echo ""
echo "📦 设置前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!
echo "前端服务 PID: $FRONTEND_PID"

echo ""
echo "========================================="
echo "✅ 服务启动成功！"
echo ""
echo "后端服务: http://localhost:8000"
echo "API文档: http://localhost:8000/api/docs"
echo "前端服务: http://localhost:3000"
echo ""
echo "测试账号:"
echo "  管理员: admin@platform.com / admin123"
echo "  长安汽车: changan@demo.com / demo123"
echo "  小易智联: xiaoyi@demo.com / demo123"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "========================================="

# 等待中断信号
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
