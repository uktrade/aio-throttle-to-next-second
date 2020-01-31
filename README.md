# aio-throttle-to-next-second [![CircleCI](https://circleci.com/gh/michalc/aiothrottler.svg?style=svg)](https://circleci.com/gh/michalc/aiothrottler) [![Test Coverage](https://api.codeclimate.com/v1/badges/e52e294a919c8974c133/test_coverage)](https://codeclimate.com/github/michalc/aiothrottler/test_coverage)

Throttler for asyncio Python that throttles to the next whole second, as reported by `time.time()`. This is useful to force an order on requests to a service that uses a "latest timestamp wins" strategy, such as S3.


## Installation

```bash
pip install aio-throttle-to-next-second
```


## Usage

Create a shared `Throttler`, with no arguments

```python
from aiothrottler import Throttler

throttler = Throttler()
```

and then just before the piece(s) of code to be throttled, _call_ this and `await` its result.

```python
await throttler()
# Each execution reaching this line will reach this line at a different second
```


## Example: multiple tasks throttled

```python
import asyncio
import time

from aiothrottler import Throttler

async def main():
    throttler = Throttler()
    await asyncio.gather(*[
        worker(throttler) for _ in range(10)
    ])

async def worker(throttler):
    await throttler()
    # Each print will show a distinct second, though all workers started together
    print(int(time.time()))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```


## Example: single task throttled/smoothed

```python
import asyncio
import random
import time

from aiothrottler import Throttler

async def main():
    throttler = Throttler()
    for _ in range(10):
        await throttler()
        # Each print will show a distinct second, though there is a random sleep
        print(int(time.time()))
        await asyncio.sleep(random.random())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```
