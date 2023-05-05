import re
import asyncio
from asyncio.events import BaseDefaultEventLoopPolicy as BasePolicy
from datetime import datetime
from functools import wraps

from rich import print as rprint

from example_01_task_factory import task_factory
from extra_01_decorator_verbose_methods_filter import verbose_methods_filter, time


ignore_methods = (
    "is_closed",
    "is_running",
    "get_debug",
    "set_debug",
    "_check_closed",
    "time",
    "_call_soon",
    "_set_coroutine_origin_tracking",
    "_add_reader",
    "_remove_reader",
    "close",
    "_close",
    "stop",
)


def verbose_loop(func):
    @wraps(func)
    def inner(*args, **kwargs):
        self = args[0]
        rprint(f"[green]{time()} Loop {func.__qualname__}")
        # rprint(f"[green]Loop {func.__qualname__} args={args[1:]}")
        # if len(self._scheduled):
        #     rprint(f"[green]    {self._scheduled=}")
        # if len(self._ready):
        #     rprint(f"[green]    {self._ready=}")
        result = func(*args, **kwargs)
        # print(f"<<< VERBOSE {func.__qualname__:30} {result=}")
        return result

    return inner


# verbose_methods = verbose_methods_filter(ignore=ignore_methods, verbose=verbose_loop)
verbose_methods = verbose_methods_filter(include=["_run_once"], verbose=verbose_loop)


@verbose_methods
class CustomLoop(type(asyncio.new_event_loop())):
    def _run_once(self):
        """Run one full iteration of the event loop.

        This calls all currently ready callbacks, polls for I/O,
        schedules the resulting callbacks, and finally schedules
        'call_later' callbacks.
        """
        # source https://github.com/python/cpython/blob/3.10/Lib/asyncio/base_events.py#L1806
        super()._run_once()


class EventLoopPolicy(BasePolicy):
    def _loop_factory(self):
        return CustomLoop()


async def dummy():
    print(f"dummy start")
    await asyncio.sleep(5)
    # task = asyncio.create_task(asyncio.sleep(1))
    # await task
    print(f"dummy stop")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(EventLoopPolicy())
    loop = asyncio.new_event_loop()
    loop.set_task_factory(task_factory)
    task1 = loop.run_until_complete(dummy())
    loop.close()
