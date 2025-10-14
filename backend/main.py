import os

import uvicorn

from app.main import app
from app.core.config import get_settings


if __name__ == "__main__":
    settings = get_settings()
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=port,
        reload=settings.environment == "development",
        log_level="info",
    )
