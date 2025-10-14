# Builda - React + FastAPI 全栈项目

一个现代化的全栈 Web 应用，使用 React + Next.js 作为前端，Python FastAPI 作为后端。

## 🚀 技术栈

### 前端
- **React 18** - 用户界面库
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全的 JavaScript
- **CSS Modules** - 样式管理

### 后端
- **Python 3.11+** - 编程语言
- **FastAPI** - 现代、快速的 Web 框架
- **Uvicorn** - ASGI 服务器
- **Pydantic** - 数据验证和设置管理

## 📁 项目结构

```
Builda/
├── frontend/                 # Next.js 前端
│   ├── src/
│   │   ├── pages/           # 页面组件
│   │   └── styles/          # 样式文件
│   ├── package.json         # 前端依赖
│   ├── tsconfig.json        # TypeScript 配置
│   ├── next.config.js       # Next.js 配置
│   └── Dockerfile          # 前端 Docker 配置
├── backend/                 # FastAPI 后端
│   ├── main.py             # 主应用文件
│   ├── requirements.txt    # Python 依赖
│   ├── env.example         # 环境变量示例
│   └── Dockerfile          # 后端 Docker 配置
├── docker-compose.yml      # Docker 编排配置
├── .gitignore             # Git 忽略文件
└── README.md              # 项目文档
```

## 🛠️ 安装和运行

### 方式一：本地开发

#### 前端
```bash
cd frontend
npm install
npm run dev
```
前端将在 http://localhost:3000 运行

#### 后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```
后端将在 http://localhost:8000 运行

### 方式二：使用 Docker

```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

访问：
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 📚 API 接口

### 基础接口
- `GET /` - 根路径
- `GET /hello` - Hello 接口
- `GET /health` - 健康检查

### 用户管理
- `GET /users` - 获取所有用户
- `POST /users` - 创建新用户
- `GET /users/{user_id}` - 根据ID获取用户
- `DELETE /users/{user_id}` - 删除用户

## 🔧 开发说明

### 前端开发
- 使用 TypeScript 确保类型安全
- 支持热重载开发
- 自动代理 API 请求到后端

### 后端开发
- 使用 FastAPI 自动生成 API 文档
- 支持 CORS 跨域请求
- 内置数据验证和错误处理

### 环境变量
复制 `backend/env.example` 为 `backend/.env` 并配置相应参数。

## 📝 开发命令

### 前端
```bash
npm run dev      # 开发模式
npm run build    # 构建生产版本
npm run start    # 启动生产版本
npm run lint     # 代码检查
```

### 后端
```bash
python main.py                    # 直接运行
uvicorn main:app --reload        # 开发模式
uvicorn main:app --host 0.0.0.0  # 生产模式
```

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

此项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果您遇到任何问题或有任何疑问，请提交 Issue 或联系维护者。
