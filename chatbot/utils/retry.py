from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry(
    *,
    retries: int,
    base_delay: float = 0.2,
    max_delay: float = 2.0,
    jitter: float = 0.1,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempt += 1
                    if attempt > retries:
                        raise
                    sleep_for = min(delay, max_delay)
                    sleep_for += random.uniform(0.0, jitter) if jitter > 0 else 0.0
                    time.sleep(sleep_for)
                    delay *= 2

        return wrapper

    return decorator

