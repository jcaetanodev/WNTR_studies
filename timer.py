import time
from dataclasses import dataclass, field
from typing import Any, ClassVar

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

@dataclass
class Timer:
    timers: ClassVar = dict()
    name: Any = None
    text: Any = "Elapsed time: {:0.4f} seconds"
    logger: Any = print
    _start_time: Any = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Initialization: add timer to dict of timers"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() -self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time