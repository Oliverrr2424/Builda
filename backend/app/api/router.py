from fastapi import APIRouter

from app.api.routes import builds, chat, feedback, health, price, products

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(products.router)
api_router.include_router(builds.router)
api_router.include_router(price.router)
api_router.include_router(feedback.router)
