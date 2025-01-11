import os
import time
import numpy as np
import tqdm

from memory_profiler.src.profiler import Profiler


def array_handler():
    """Runs a loop to create an array and keep it in memory for 1 second and then delete it"""
    for __ in tqdm.tqdm(range(5)):
        array = np.ones((50000, 2000), dtype=np.float32)  # 400 MB
        time.sleep(1)
        del array
        time.sleep(1)


if __name__ == "__main__":
    
    pid = os.getpid()

    profiler = Profiler(pid, "my_function")
    profiler.start()

    array_handler()

    # If monitor is not specified, all metrics will be logged
    # Logged metrics are data, rss, swap, uss
    profiler.save(monitor=None)
    profiler.plot(monitor=None)
