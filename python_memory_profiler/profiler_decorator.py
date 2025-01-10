import psutil
import sys
import os
import time

from .src.profiler import Profiler

if not (psutil.LINUX or psutil.MACOS or psutil.WINDOWS):
    sys.exit("platform not supported")


def profile_memory_decorator(function):
    """
    A decorator to profile memory usage of a function.

    This decorator uses the `Profiler` class to monitor memory usage during the
    execution of the decorated function, saves the profiling data, and generates
    corresponding plots.

    Args:
        function (callable): The function to be profiled.

    Returns:
        callable: A wrapped function that profiles memory usage during execution.

    Notes:
        - The memory profiling process begins before the function execution and
          continues until shortly after it completes.
        - Memory data is saved for the "data" metric only.
        - A plot of memory usage over time is generated and saved in the specified directory.
    """

    def wrapper():
        pid = os.getpid()
        profiler_instance = Profiler(pid, function.__name__)
        profiler_instance.start()
        # Give some time to the profiler to initialize
        time.sleep(0.1)
        function()
        time.sleep(0.1)
        profiler_instance.save("data")
        profiler_instance.plot("data")

    return wrapper
