import logging.config
from os import path

import uvicorn
from fastapi import FastAPI
from controllers.routes.auth import router as auth_router
from controllers.routes.test import router as test_router

from config import settings
from controllers.middleware import HandleHTTPErrorsMiddleware, CORSMiddlewareCustom

log_file_path = path.join(path.dirname(path.abspath(__file__)), "log_config.ini")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logging.getLogger().setLevel(settings.LOG_LEVEL)

app = FastAPI(title="Banners")

# Middlewares
app.add_middleware(HandleHTTPErrorsMiddleware)
app.add_middleware(CORSMiddlewareCustom)

# Reports routes
app.include_router(auth_router, tags=["auth"])
app.include_router(test_router, tags=["test"])

if __name__ == "__main__":
    uvicorn.run(app, reload=True)
