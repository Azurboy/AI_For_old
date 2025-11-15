#!/bin/bash

# 语客颂 - 一键启动脚本

echo "🚀 启动语客颂项目..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

echo "📦 检查依赖..."

# 安装后端依赖
if [ ! -d "backend/env" ]; then
    echo "   安装后端依赖..."
    cd backend
    pip3 install -r requirements.txt > /dev/null 2>&1
    cd ..
fi

# 安装前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "   安装前端依赖..."
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
fi

echo "✅ 依赖检查完成"
echo ""

# 检查.env文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 backend/.env 文件"
    echo "   复制 .env.example 并配置API密钥..."
    cp backend/.env.example backend/.env
    echo "   请编辑 backend/.env 文件填入你的API密钥"
    echo ""
fi

# 启动后端
echo "🔧 启动后端服务 (http://localhost:8000)..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端应用 (http://localhost:3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# 启动仪表盘
echo "📊 启动演示仪表盘 (http://localhost:8080)..."
cd dashboard
python3 -m http.server 8080 > /dev/null 2>&1 &
DASHBOARD_PID=$!
cd ..

echo ""
echo "✅ 所有服务已启动！"
echo ""
echo "📱 老人端App:     http://localhost:3000"
echo "📊 演示仪表盘:    http://localhost:8080"
echo "🔌 后端API:       http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID $DASHBOARD_PID 2>/dev/null; echo ''; echo '👋 服务已停止'; exit 0" INT

wait

