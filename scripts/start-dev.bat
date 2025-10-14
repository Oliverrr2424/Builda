@echo off
echo 启动 Builda 开发环境...

echo 启动后端服务...
cd backend
start "Backend" cmd /k "python main.py"

echo 等待后端启动...
timeout /t 3 /nobreak > nul

echo 启动前端服务...
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo 开发环境启动完成！
echo 前端: http://localhost:3000
echo 后端: http://localhost:8000
echo API 文档: http://localhost:8000/docs

pause
