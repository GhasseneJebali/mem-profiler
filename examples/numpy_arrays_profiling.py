import time
import numpy as np
import tqdm
from python_memory_profiler.tools import profile_memory_decorator


@profile_memory_decorator
def array_handler():
    for idx in tqdm.tqdm(range(5)):
        array = np.ones((10000, 10000), dtype=np.float32)  # 381.47 MB
        time.sleep(1)
        del array
        time.sleep(1)
    array = np.ones((5000, 10000), dtype=np.float32)
    time.sleep(1)
    del array


# In a terminal, run "python numpy_arrays_profiling.py"
array_handler()
