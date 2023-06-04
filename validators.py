from typing import Literal

from fastapi import Request, HTTPException

from loguru import logger
from redis_r import redis_cli
from config import BREACH_TOKEN, CONNECT_TOKEN, UPDATE_TOKEN, ACTIVATE_TOKEN, SHUTDOWN_TOKEN, GET_TOKEN, GET_DATA_TOKEN


def __validate_token(key: str, token: str) -> bool:
    return key == token


def validate_breach_token(token: str):
    return __validate_token(key=BREACH_TOKEN, token=token)


def validate_activate_token(token: str):
    return __validate_token(key=ACTIVATE_TOKEN, token=token)


def validate_shutdown_token(token: str):
    return __validate_token(key=SHUTDOWN_TOKEN, token=token)


def validate_connect_token(token: str):
    return __validate_token(key=CONNECT_TOKEN, token=token)


def validate_get_token(token: str):
    return __validate_token(key=GET_TOKEN, token=token)


def validate_get_data_token(token: str):
    return __validate_token(key=GET_DATA_TOKEN, token=token)


def validate_update_token(token: str):
    return __validate_token(key=UPDATE_TOKEN, token=token)


def validate_session_token(token: str):
    keys = redis_cli.keys("*")
    return token in keys


validate_mapping = {
    "breach": validate_breach_token,
    "activate": validate_activate_token,
    "update": validate_update_token,
    "connect": validate_connect_token,
    "shutdown": validate_shutdown_token,
    "session": validate_session_token,
    "get": validate_get_token,
    "get_data": validate_get_data_token,
}


def validate_tokens(
        tokens: dict[Literal[
            "breach", "activate", "connect", "update", "shutdown", "session", "get", "get_data"
        ], str],
        request: Request
):
    for token_type, token in tokens.items():
        access = validate_mapping[token_type](token=token)
        if not access:
            message = f"{request.url}: \n Wrong {token_type} token! {request.client}."
            logger.warning(message)
            raise HTTPException(404)
        
