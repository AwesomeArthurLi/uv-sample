from datetime import datetime, timedelta
import logging
import math
import time
from sample.tools import timed_lru_cache, Authentication


def test_timed_lru_cache():
    @timed_lru_cache(seconds=5)
    def test_func():
        return f'it is refreshed {datetime.now().strftime("%H:%M:%S")}'

    for i in range(20):
        logging.info(f"current is  {i} \t {test_func()}")

        time.sleep(1)


def test_Authentication_with_default_cached_timedelta():
    previous_user = None
    previous_token = None
    step = 5
    for i in range(1, 50):
        auth = Authentication("u1", "p1", "cid01", "cs01")
        logging.info(f"user: {auth.user}")
        logging.info(f"token: {auth.token}")
        time.sleep(1)

        if previous_user is not None:
            if i % step == 1:
                assert (auth.user - previous_user).seconds == step
            else:
                assert (auth.user - previous_user).seconds == 0

            if i % (step * 2) == 1:
                logging.info(f"################# {i} \t auth.token: {auth.token} \t previous_token: {previous_token} ")
                assert (auth.token - previous_token).seconds == step * 2
            else:
                assert (auth.token - previous_token).seconds == 0

        previous_user = auth.user
        previous_token = auth.token


def test_Authentication_with_customized_cached_timedelta():
    previous_user = None
    previous_token = None
    step = 8
    for i in range(1, 50):
        auth = Authentication(
            username="u1",
            password="p1",
            client_id="cid01",
            client_secret="cs01",
            result_cached_seconds=step,
        )
        logging.info(f"user: {auth.user}")
        logging.info(f"token: {auth.token}")
        time.sleep(1)

        if previous_user is not None:
            # for token - cached 10 s
            if i % step == 1:
                logging.info(f"################# {i} \t auth.token: {auth.token} \t previous_token: {previous_token} ")
                logging.info(f"################# {i} \t auth.user : {auth.user} \t  previous_user : {previous_user} ")
                assert (auth.user - previous_user).seconds == step
                assert (auth.token - previous_token).seconds == step
            else:
                logging.info(f"################# {i} \t auth.user : {auth.user} \t  previous_user : {previous_user} ")
                logging.info(f"################# {i} \t auth.token: {auth.token} \t previous_token: {previous_token} ")
                assert (auth.user - previous_user).seconds == 0
                assert (auth.token - previous_token).seconds == 0
            # # for user - cached 5 s
            # if i % step == 1 and i > step / 2:

            #     logging.info(f"################# {i} \t auth.user : {auth.user} \t  previous_user : {previous_user} ")
            #     assert (auth.user - previous_user).seconds == step
            # else:
            #     logging.info(f"################# {i} \t auth.user : {auth.user} \t  previous_user : {previous_user} ")
            #     assert (auth.user - previous_user).seconds == 0
        previous_user = auth.user
        previous_token = auth.token
