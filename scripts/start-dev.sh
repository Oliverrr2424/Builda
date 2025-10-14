#!/bin/bash

echo "启动 Builda 开发环境..."

# 检查 Node.js 和 Python 是否安装
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python"
    exit 1
fi

# 启动后端
echo "启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!

# 等待后端启动
echo "等待后端启动..."
sleep 3

# 启动前端
echo "启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "开发环境启动完成！"
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
