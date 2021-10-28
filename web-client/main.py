# Copyright INRIM (https://www.inrim.eu)
# See LICENSE file for full licensing details.
import logging
import os
import string
import time
import uuid
from functools import lru_cache
import requests

from fastapi import FastAPI, Request, Header, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse

from models import *
import time as time_
from settings import get_settings, templates
import httpx

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from core.Gateway import Gateway
from core.ContentService import ContentService
from core.AuthService import AuthContentService
from core.AttachmentService import AttachmentService
from core.MailService import MailService
from core.ImportService import ImportService
from core.SystemService import SystemService

import ujson
from fastapi.templating import Jinja2Templates

from client_api import client_api
import importlib

logger = logging.getLogger(__name__)

# dynamic import module
for plugin in get_settings().plugins:
    try:
        importlib.import_module(plugin)
    except ImportError as e:
        logger.error(f"Error import module: {plugin} msg: {e} ")

# from inrim.base_theme.ThemeConfigInrim import ThemeConfigInrim


tags_metadata = [
    {
        "name": ":-)",
        "description": "Forms Inrim",
    },
    {
        "name": "base",
        "description": "API Base",
    },
]

responses = {
    401: {
        "description": "Token non valido",
        "content": {"application/json": {"example": {"detail": "Auth invalid"}}}},
    422: {
        "description": "Dati richiesta non corretti",
        "content": {"application/json": {"example": {"detail": "err messsage"}}}}
}

app = FastAPI(
    title=get_settings().app_name,
    description=get_settings().app_desc,
    version="1.0.0",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.mount("/static", StaticFiles(directory=f"core/themes/{get_settings().theme}/static"), name="static")
app.mount("/client", client_api)


# app.mount("/design", builder_api)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid.uuid4())
    logger.info(f"rid={idem} start request path={request.url.path},req_id={request.headers.get('req_id')}")
    start_time = time_.time()

    response = await call_next(request)

    process_time = (time_.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}, "
        f"req_id={response.headers.get('req_id')}"
    )
    if response.status_code == 404:
        return RedirectResponse("/")
    return response


@app.get("/status", tags=["base"])
async def service_status():
    """
    Ritorna lo stato del servizio
    """
    return {"status": "live"}


@app.get("/favicon.ico", tags=["base"])
async def favicon():
    """
    Ritorna lo stato del servizio
    """
    RedirectResponse("/static/favicon/favicon.ico")


def deserialize_header_list(request):
    list_data = request.headers.mutablecopy().__dict__['_list']
    res = {item[0].decode("utf-8"): item[1].decode("utf-8") for item in list_data}
    return res.copy()


@app.get("/login/", tags=["base"])
async def login(
        request: Request,
):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    auth_service = ContentService.new(gateway=gateway, remote_data={})
    return await auth_service.get_login_page()


@app.get("/login", tags=["base"])
async def login(
        request: Request,
):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    auth_service = ContentService.new(gateway=gateway, remote_data={})
    return await auth_service.get_login_page()


@app.post("/login", tags=["base"])
async def login(
        request: Request,
):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    # auth_service = ContentService.new(gateway=gateway, remote_data={})
    return await gateway.server_post_action()


@app.post("/{path:path}")
async def proxy_post(request: Request, path: str):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    return await gateway.server_post_action()


@app.get("/{path:path}")
async def proxy_req(request: Request, path: str):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    return await gateway.server_get_action()


@app.delete("/{path:path}")
async def proxy_delete(request: Request, path: str):
    gateway = Gateway.new(request=request, settings=get_settings(), templates=templates)
    return await gateway.server_delete_action()


@app.on_event("startup")
async def startup_event():
    sys_service = SystemService.new(settings=get_settings(), templates=templates)
    await sys_service.check_and_init_service()
