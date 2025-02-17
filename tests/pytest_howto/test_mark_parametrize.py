from datetime import datetime
import logging
import time
import pytest


def double(i: int) -> int:
    return i * 2


@pytest.mark.parametrize(
    "i, expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
        (10, 20),
        (0, 0),
    ],
)
def test_double(i: int, expected: int) -> None:
    assert double(i) == expected


@pytest.mark.parametrize("i", range(7))
def test_range(i):
    if i not in (0, 1, 2, 3, 4, 5, 6):
        pytest.fail("i is not in range")


@pytest.mark.xfail(reason="bad luck")
@pytest.mark.parametrize("i", range(7))
def test_range(i):
    if i in (1, 6):
        pytest.fail("bad luck")


# uv add --dev pytest-timeout
@pytest.mark.timeout(10)
def test_timeout():
    start = datetime.now()
    time.sleep(11)
    delta = datetime.now() - start
    logging.info(f"it costs {delta.seconds}")
