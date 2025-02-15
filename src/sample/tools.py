from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
import logging
import time


def timed_lru_cache(_func=None, *, seconds: int = 7000, maxsize: int = 1, typed: bool = False):
    """Extension over existing lru_cache with timeout
    :param seconds: timeout value or it will use the result_cached_seconds if the func has set this parameter.
    :param maxsize: maximum size of the cache
    :param typed: whether different keys for different types of cache keys
    """

    def wrapper_cache(f):
        # create a function wrapped with traditional lru_cache
        f = lru_cache(maxsize=maxsize, typed=typed)(f)
        f.delta = seconds
        f.expiration = time.monotonic() + f.delta
        f.customized_flag = False

        def wrapped_f(*args, **kwargs):
            new_delta = kwargs.get("result_cached_seconds")
            # logging.info(f"the new delta is {new_delta}")
            if new_delta and isinstance(new_delta, (int, float)) and not f.customized_flag:
                f.cache_clear()
                # logging.info(f"the result_cached_seconds is {new_delta}")
                f.delta = new_delta
                f.customized_flag = True
                f.expiration = time.monotonic() + f.delta
            if time.monotonic() >= f.expiration:
                # if the current cache expired of the decorated function then
                # clear cache for that function and set a new cache value with new expiration time
                f.cache_clear()
                f.expiration = time.monotonic() + f.delta
            return f(*args, **kwargs)

        wrapped_f.cache_info = f.cache_info
        wrapped_f.cache_clear = f.cache_clear
        return wrapped_f

    # To allow decorator to be used without arguments
    if _func is None:
        return wrapper_cache
    else:
        return wrapper_cache(_func)


@dataclass
class Authentication:
    username: str
    password: str

    token: str
    user: str

    def __init__(self, username: str = None, password: str = None, client_id: str = None, client_secret: str = None):
        self.user = user_login(username, password)
        self.token = token(client_id, client_secret)


@timed_lru_cache(seconds=5)
def user_login(username: str, password: str, **kwargs):
    now = datetime.now()
    logging.info(f'user:  {now.strftime("%H:%M:%S")}')
    return now


@timed_lru_cache(seconds=10)
def token(client_id: str, client_secret: str, **kwargs) -> datetime:
    now = datetime.now()
    logging.info(f'token: {now.strftime("%H:%M:%S")}')
    return now


class Authentication:
    username: str
    password: str

    token: datetime
    user: datetime

    def __init__(
        self, username: str = None, password: str = None, client_id: str = None, client_secret: str = None, **kwargs
    ):
        self.user = user_login(username, password, **kwargs)
        self.token = token(client_id, client_secret, **kwargs)
