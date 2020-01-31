import asyncio
from asyncio import (
    Event,
    ensure_future,
    get_event_loop,
)
from math import (
    floor,
)
from time import (
    time,
)
from unittest import (
    TestCase,
)
from unittest import (
    TestCase,
)

from aio_throttle_to_next_second import (
    Throttler,
)


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = get_event_loop()
        loop.run_until_complete(future)
    return wrapper


def is_at_or_just_after(time_b, time_a):
    return time_a <= time_b < time_a + 0.01


class TestThrottler(TestCase):

    @async_test
    async def test_tasks_queued_immediately_at_whole_second(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        now = time()
        time_at_next_second = floor(now + 1.0)
        time_to_next_second = max(0, time_at_next_second - now)
        await asyncio.sleep(time_to_next_second)

        time_a = time()
        time_b = floor(time_a + 1.0)
        time_c = time_b + 1

        throttler = Throttler()

        event_a = Event()
        task_a = ensure_future(func(throttler(), event_a))

        event_b = Event()
        task_b = ensure_future(func(throttler(), event_b))

        event_c = Event()
        task_c = ensure_future(func(throttler(), event_c))

        await event_a.wait()

        self.assertTrue(is_at_or_just_after(time(), time_a))

        await event_b.wait()

        self.assertTrue(is_at_or_just_after(time(), time_b))

        await event_c.wait()

        self.assertTrue(is_at_or_just_after(time(), time_c))

    @async_test
    async def test_tasks_queued_immediately_at_mid_second(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        now = time()
        time_at_next_second = floor(now + 1.0)
        time_to_next_second = max(0, time_at_next_second - now)
        await asyncio.sleep(time_to_next_second + 0.5)

        time_a = time()
        time_b = floor(time_a + 1.0)
        time_c = time_b + 1

        throttler = Throttler()

        event_a = Event()
        task_a = ensure_future(func(throttler(), event_a))

        event_b = Event()
        task_b = ensure_future(func(throttler(), event_b))

        event_c = Event()
        task_c = ensure_future(func(throttler(), event_c))

        await event_a.wait()

        self.assertTrue(is_at_or_just_after(time(), time_a))

        await event_b.wait()

        self.assertTrue(is_at_or_just_after(time(), time_b))

        await event_c.wait()

        self.assertTrue(is_at_or_just_after(time(), time_c))

    @async_test
    async def test_tasks_queued_immediately_various_offsets(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        for i in range(0, 10):
            await asyncio.sleep(0.1 * i)

            time_a = time()
            time_b = floor(time_a + 1.0)
            time_c = time_b + 1

            throttler = Throttler()

            event_a = Event()
            task_a = ensure_future(func(throttler(), event_a))

            event_b = Event()
            task_b = ensure_future(func(throttler(), event_b))

            event_c = Event()
            task_c = ensure_future(func(throttler(), event_c))

            await event_a.wait()

            self.assertTrue(is_at_or_just_after(time(), time_a))

            await event_b.wait()

            self.assertTrue(is_at_or_just_after(time(), time_b))

            await event_c.wait()

            self.assertTrue(is_at_or_just_after(time(), time_c))

    @async_test
    async def test_tasks_queued_later(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        for i in range(0, 10):
            await asyncio.sleep(0.1 * i)

            time_a = time()
            throttler = Throttler()

            event_a = Event()
            task_a = ensure_future(func(throttler(), event_a))

            await event_a.wait()

            self.assertTrue(is_at_or_just_after(time(), time_a))

            await asyncio.sleep(0.5)

            now = time()
            time_b = \
                now if int(now) > int(time_a) else \
                floor(time_a + 1.0)
            time_c = floor(time_b + 1.0)

            event_b = Event()
            task_b = ensure_future(func(throttler(), event_b))

            event_c = Event()
            task_c = ensure_future(func(throttler(), event_c))

            await event_b.wait()

            self.assertTrue(is_at_or_just_after(time(), time_b))

            await event_c.wait()

            self.assertTrue(is_at_or_just_after(time(), time_c))

    @async_test
    async def test_tasks_cancelled(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        for i in range(0, 10):
            await asyncio.sleep(0.1 * i)

            time_a = time()
            time_d = floor(time_a + 1.0)

            throttler = Throttler()

            event_a = Event()
            task_a = ensure_future(func(throttler(), event_a))
            task_b = ensure_future(func(throttler(), Event()))
            task_c = ensure_future(func(throttler(), Event()))
            event_d = Event()
            task_d = ensure_future(func(throttler(), event_d))

            await event_a.wait()

            task_b.cancel()
            task_c.cancel()

            await event_d.wait()

            self.assertTrue(is_at_or_just_after(time(), time_d))

    @async_test
    async def test_final_task_cancelled(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        for i in range(0, 10):
            await asyncio.sleep(0.1 * i)

            time_a = time()
            time_d = floor(time_a + 1.0)

            throttler = Throttler()

            event_a = Event()
            task_a = ensure_future(func(throttler(), event_a))
            task_b = ensure_future(func(throttler(), Event()))

            await event_a.wait()

            task_b.cancel()

            event_d = Event()
            task_d = ensure_future(func(throttler(), event_d))

            await event_d.wait()

            self.assertTrue(is_at_or_just_after(time(), time_d))

    @async_test
    async def test_no_throttle_if_not_need_to(self):
        loop = get_event_loop()

        async def func(throttle, event):
            await throttle
            event.set()

        for i in range(0, 10):
            await asyncio.sleep(0.1 * i)

            time_a = time()

            throttler = Throttler()

            event_a = Event()
            task_a = ensure_future(func(throttler(), event_a))

            await event_a.wait()
            self.assertTrue(is_at_or_just_after(time(), time_a))

            await asyncio.sleep(1.2)

            time_b = time()
            event_b = Event()
            task_b = ensure_future(func(throttler(), event_b))

            await event_b.wait()
            self.assertTrue(is_at_or_just_after(time(), time_b))

            await asyncio.sleep(1.2)

            time_c = time()
            event_c = Event()
            task_c = ensure_future(func(throttler(), event_c))

            await event_c.wait()
            self.assertTrue(is_at_or_just_after(time(), time_c))
