#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: main.py
@Created: 2023/3/3 12:49
"""
from fastapi import FastAPI
from loguru import logger

from server import views_repo, views_task
from server.core.host import local_host
from utils import config

PORT = 5555
app = FastAPI()
# 注册路由
app.include_router(views_repo.router)
app.include_router(views_task.router)


@app.on_event("startup")
def startup_event():
    if config.host.remote:
        logger.info("你选择将执行机注册到平台上")
        local_host.port = PORT
        local_host.register()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=PORT, reload=True)
