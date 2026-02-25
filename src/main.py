import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

import src.consts as consts
from src.responses.base import ErrorResponse
from src.utils.methods import init
from src.utils.strings import Strings
from src.v1.router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # on_startup
    # make folder if not exist yet
    if not os.path.isdir(consts.DOWNLOAD_LOC):
        os.mkdir(consts.DOWNLOAD_LOC)

    # prompt user for oauth
    init()

    # give back control to fastapi
    yield


app = FastAPI(
    title="Gator Tune Music Service",
    description="The external service for fetching musics",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=consts.ALLOW_METHODS.split(","),
    allow_origins=consts.ALLOW_ORIGINS.split(","),
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Main"])
def health():
    return Strings.HEALTH


app.include_router(router)


@app.exception_handler(Exception)
def global_error_handler(_, exc: Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            Strings.INTERNAL_ERROR.format(exc),
            exc.__class__.__name__,
            status_code,
        ).__dict__,
    )
