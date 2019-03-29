from asyncio import (
    Future,
    TimerHandle,
    get_event_loop,
)
from collections import (
    deque
)


def Throttler(wait):
    loop = get_event_loop()
    queued = deque()
    last_resolved = loop.time() - wait
    callback = None

    def schedule_callback():
        nonlocal callback
        wait_required = max(0, wait - (loop.time() - last_resolved))
        callback = loop.call_later(wait_required, resolve)

    def resolve():
        nonlocal callback
        nonlocal last_resolved

        callback = None

        while queued and queued[0].cancelled():
            queued.popleft()

        if queued:
            future = queued.popleft()
            future.set_result(None)
            last_resolved = loop.time()

        if queued:
            schedule_callback()

    def throttler():
        future = Future()
        queued.append(future)

        if callback is None:
            schedule_callback()

        return future

    return throttler
