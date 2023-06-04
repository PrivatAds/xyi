from typing import Literal
from loguru import logger

from redis import Redis

from config import MAX_SESSIONS

redis = Redis(host="localhost", port=6379, decode_responses=True)

def get_all_session_keys() -> list:
    keys = redis.keys("*")
    session_keys = []
    for key in keys:
        if "sessions:" in key:
            session_keys.append(key.replace("sessions:", ""))
    return session_keys


def set_status(key: str, status: str) -> None:
    redis.hset(f"sessions:{key}", "status", status)


def del_all_keys() -> list:
    keys = redis.keys('*')
    if keys:
        redis.delete(*keys)
        return keys
    return []

def get_available_session_keys() -> list:
    sessions = get_all_session_keys()
    available_session_keys = []
    for session_key in sessions:
        session_status = redis.hget(f"sessions:{session_key}", "status")
        if session_status == "available":
            available_session_keys.append(session_key)
    
    return available_session_keys


def get_pre_session_keys() -> list:
    sessions = get_all_session_keys()
    pre_session_keys = []
    for session_key in sessions:
        session_status = redis.hget(f"sessions:{session_key}", "status")
        if session_status == "pre":
            pre_session_keys.append(session_key)

    return pre_session_keys


def is_new_session_required() -> bool:

    pre_len = len(get_pre_session_keys())
    available_len  = len(get_available_session_keys())

    total_len = pre_len + available_len

    logger.info(f"Pre + available: {pre_len} + {available_len} / {MAX_SESSIONS}")

    return total_len < MAX_SESSIONS


def lock_session(session_key: str) -> None:
    redis.hset(f"sessions:{session_key}", "status", "locked")


def create_session(key: str, data: str) -> None:
    mapping = {"data": data, "status": "pre"}
    redis.hset(f"sessions:{key}", mapping=mapping)


def update_session(key: str, data: str) -> str:

    keys = get_all_session_keys()
    if key not in keys:
        return "error"
    else:
        mapping = {"data": data, "status": "available"}
        redis.hset(f"sessions:{key}", mapping=mapping)

    
def delete_session(key: str) -> str:
    
    keys = get_all_session_keys()
    if key not in keys:
        return "error"
    else:
        redis.delete(f"sessions:{key}")


def get_session() -> str:
    session_keys = get_available_session_keys()
    if len(session_keys):
        session_key = session_keys[0]
        lock_session(session_key=session_key)
        logger.info(f"Got session {session_key}!")
        return session_key
    else:
        return "error"


def get_session_data(key: str):
    if key not in get_all_session_keys():
        return "error"
    else:
        data = redis.hget(f"sessions:{key}", "data")
        return data