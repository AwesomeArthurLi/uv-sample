from datetime import datetime
import logging
import time
from sample.tools import timed_lru_cache, Authentication


def test_timed_lru_cache():
    @timed_lru_cache(seconds=5)
    def test_func():
        return f'it is refreshed {datetime.now().strftime("%H:%M:%S")}'

    for i in range(20):
        logging.info(f"current is  {i} \t {test_func()}")

        time.sleep(1)


def test_Authentication():
    for i in range(1, 50):
        auth = Authentication("u1", "p1", "cid01", "cs01")
        logging.info(f"user: {auth.user}")
        logging.info(f"token: {auth.token}")
        time.sleep(1)
        if i % 5 == 0:
            logging.info("################# 5 ##############")
