import os
import re
import subprocess
from contextlib import asynccontextmanager
from textwrap import dedent
from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from src.responses.base import ErrorResponse
from src.utils import consts
from src.utils.methods import init
from src.utils.strings import Strings
from src.v2.router import router as routerv2
from src.v2.service import YT

version = "<git executable not installed>"
message = "<git executable not installed>"

try:
    git_log = subprocess.check_output(["git", "log", "-n", "1"]).decode("ascii").strip()

    re_version: str = r"(?<=commit\s)\w+"
    re_message: str = r"(?<=\n\n).+"

    version = re.findall(re_version, git_log)[0].strip()[:7]
    message = re.findall(re_message, git_log)[0].strip()
except Exception:  # noqa
    pass


@asynccontextmanager
async def lifespan(_: FastAPI):
    # on_startup
    # make folder if not exist yet
    if not os.path.isdir(consts.DOWNLOAD_LOC):
        os.mkdir(consts.DOWNLOAD_LOC)

    # init
    init()

    # give back control to fastapi
    yield


description = f"""
The external service for fetching musics <br />
commit {version} - {message}
"""

app = FastAPI(
    title="Gator Tune Music Service",
    description=(dedent(description)),
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
def health(service: Annotated[YT, Depends(YT)]):
    return service.health()


app.include_router(routerv2)


@app.exception_handler(ErrorResponse)
def custom_error_handler(_, exc: ErrorResponse):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.__dict__,
    )


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
