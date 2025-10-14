from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="Builda API",
    description="React + Next.js 前端 + Python FastAPI 后端",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class Message(BaseModel):
    message: str

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

# 模拟数据库
users_db = []
user_counter = 1

@app.get("/")
async def root():
    """根路径"""
    return {"message": "欢迎使用 Builda API！", "version": "1.0.0"}

@app.get("/hello")
async def hello():
    """Hello 接口"""
    return {"message": "Hello from FastAPI! 后端连接成功！"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}

@app.get("/users", response_model=List[User])
async def get_users():
    """获取所有用户"""
    return users_db

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """创建新用户"""
    global user_counter
    new_user = User(
        id=user_counter,
        name=user.name,
        email=user.email
    )
    users_db.append(new_user)
    user_counter += 1
    return new_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据ID获取用户"""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="用户未找到")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return {"message": f"用户 {deleted_user.name} 已删除"}
    raise HTTPException(status_code=404, detail="用户未找到")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
