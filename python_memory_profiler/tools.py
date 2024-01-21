import psutil
import sys
import os
import time

from .profiler import Profiler

if not (psutil.LINUX or psutil.MACOS or psutil.WINDOWS):
    sys.exit("platform not supported")


def profile_memory_decorator(function):
    def wrapper():
        pid = os.getpid()
        profiler_instance = Profiler(pid, function.__name__)
        profiler_instance.start()
        # Give some time to the profiler to initialize
        time.sleep(0.1)
        function()
        time.sleep(0.1)
        profiler_instance.save()
        profiler_instance.plot("data")

    return wrapper
