import time
import numpy as np
import tqdm
from memory_profiler.decorators import memory_profiler_decorator


@memory_profiler_decorator
def array_handler():
    """
    Runs a loop to create an array and keep it in memory for 1 second
    and then delete it
    """
    for __ in tqdm.tqdm(range(5)):
        array = np.ones((50000, 1000), dtype=np.float32)  # 200 MB
        time.sleep(1)
        del array
        time.sleep(1)
    array = np.ones((25000, 1000), dtype=np.float32)  # 100 MB
    time.sleep(1)
    del array


if __name__ == "__main__":
    array_handler()
