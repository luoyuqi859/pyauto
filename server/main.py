#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: main.py
@Created: 2023/3/3 12:49
"""
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from server import views_repo, views_task, views_device
from server.core.host import local_host
from utils import config

PORT = 5555
app = FastAPI(title="FastApi执行机")
# 注册路由
app.include_router(views_repo.router)
app.include_router(views_task.router)
app.include_router(views_device.router)


@app.on_event("startup")
def startup_event():
    if config.host.remote:
        logger.info("你选择将执行机注册到平台上")
        local_host.port = PORT
        local_host.register()


@app.get('/ping')
def pong():
    return "pong"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=PORT)
