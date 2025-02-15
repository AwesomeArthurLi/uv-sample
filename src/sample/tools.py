from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
import time


def timed_lru_cache(_func=None, *, seconds: int = 7000, maxsize: int = 1, typed: bool = False):
    """Extension over existing lru_cache with timeout
    :param seconds: timeout value
    :param maxsize: maximum size of the cache
    :param typed: whether different keys for different types of cache keys
    """

    def wrapper_cache(f):
        # create a function wrapped with traditional lru_cache
        f = lru_cache(maxsize=maxsize, typed=typed)(f)
        # convert seconds to nanoseconds to set the expiry time in nanoseconds
        f.delta = seconds
        f.expiration = time.monotonic() + f.delta

        def wrapped_f(*args, **kwargs):
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
def user_login(username: str, password: str):
    return f'{datetime.now().strftime("%H:%M:%S")}'


@timed_lru_cache(seconds=10)
def token(client_id: str, client_secret: str):
    return f'{datetime.now().strftime("%H:%M:%S")}'
