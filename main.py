from typing import Literal, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from loguru import logger

from redis_funcs import get_all_session_keys, is_new_session_required, create_session, update_session, delete_session, get_session, get_session_data, set_status, del_all_keys
from utils import generate_random_code, validate_token, decrypt_data

from config import IS_ACTIVE, REDIRECT_URL

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class SessionCreateQuery(BaseModel):
    encrypted_data: Optional[str]


class SessionUpdateQuery(BaseModel):
    key: str
    encrypted_data: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if IS_ACTIVE:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(REDIRECT_URL)


@app.get("/is-free-slot")
async def is_free(token: str) -> dict[str, str]:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)
    
    if is_new_session_required():
        return {"status": "True"}
    else:
        return {"status": "False"}


@app.delete("/delkeys")
async def delkeys(token: str) -> dict[str, str]:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)
    
    deleted_keys = del_all_keys()
    return {"deleted_keys": str(deleted_keys)}
    

# Client endpoints
@app.post("/create-session")
async def create(token: str, query: SessionCreateQuery, request: Request) -> dict:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)

    all_sessions = get_all_session_keys()

    code = generate_random_code()
    while code in all_sessions:
        code = generate_random_code()

    if query.encrypted_data:
        encrypted_data = query.encrypted_data
        decrypted_data = decrypt_data(encrypted_data)
    else:
        decrypted_data = ""

    create_session(key=code, data=decrypted_data)

    logger.info(f"Session {code} created!")

    return {"key": code}


@app.post("/update-session")
async def update(token: str, query: SessionUpdateQuery, request: Request) -> dict:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)

    encrypted_data = query.encrypted_data
    decrypted_data = decrypt_data(encrypted_data)

    result = update_session(key=query.key, data=decrypted_data)
    if result == "error":
        raise HTTPException(404, "No such session!")
    else:
        logger.info(f"Session {query.key} data updated!")
        return {"msg": f"Session {query.key} data is now {query.encrypted_data}"}


@app.delete("/delete-session")
async def delete(token: str, key: str):

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)

    result = delete_session(key=key)
    if result == "error":
        raise HTTPException(404, "No such session!")
    logger.info(f"Session {key} deleted!")
    return {"msg": f"Session {key} deleted!" }


# Frontend endpoints
@app.get("/get-session")
async def get(token: str, request: Request) -> str:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)

    result = get_session()
    if result =="error":
        raise HTTPException(404, "No active sessions")
    else:
        return result


@app.get("/get-session-data")
async def get_data(token: str, session_key: str, request: Request) -> str:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)

    if not session_key:
        return ""
    else:
        result = get_session_data(key=session_key)
        if result == "error":
            raise HTTPException(404, "No such session!")
        else:
            return result
    

@app.get("/unlock-session")
async def unlock(token: str, session_key: str) -> None:

    access = validate_token(token=token)
    if not access:
        raise HTTPException(404)
    
    set_status(key=session_key, status="available")
    logger.info(f"Session {session_key} unlocked!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="error")