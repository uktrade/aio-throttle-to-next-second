from asyncio import (
    Future,
    get_event_loop,
)
from collections import (
    deque,
)
from math import (
    floor,
)
from time import (
    time,
)


def Throttler():
    loop = get_event_loop()
    queued = deque()
    last_resolved = floor(time() - 1.0)
    resolve_callback = None

    def schedule_resolve():
        nonlocal resolve_callback

        now = time()
        time_at_next_second = floor(last_resolved + 1.0)
        time_to_next_second = max(0, time_at_next_second - now)
        resolve_callback = loop.call_later(time_to_next_second, resolve)

    def resolve():
        nonlocal resolve_callback
        nonlocal last_resolved

        resolve_callback = None

        while queued and queued[0].cancelled():
            queued.popleft()

        if queued:
            queued.popleft().set_result(None)
            last_resolved = time()

        if queued:
            schedule_resolve()

    def throttler():
        future = Future()
        queued.append(future)

        if resolve_callback is None:
            schedule_resolve()

        return future

    return throttler
