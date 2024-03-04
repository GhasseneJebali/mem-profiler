# mem-profiler
A lightweight project for RAM consumption profiling over the time.

This project is intended for personal usage for now since the more notorious memory-profiler package is no longer maintained and issues will not be resolved.

**If you have any ideas, remarques or you want to contribute, do not hesitate to ping me or to create a pull request or a ticket. I will gladly have a look at it.**

The objective of this project is to provide a decorator capable of tracking RAM consumption of a function over the time and to plot and save the results into an image.

**Command line to install the package from source with requirments:**
```bash
cd mem-profiler
pip install -e .
```

**Example of how to use the profiler decorator:**
```python
import time
import numpy as np
import tqdm
from python_memory_profiler.tools import profile_memory_decorator


@profile_memory_decorator
def array_handler():
    """ Run a loop to create an array and keep it in memory for 1 second and then delete it"""
    for idx in tqdm.tqdm(range(5)):
        array = np.ones((10000, 10000), dtype=np.float32)  # 381.47 MB
        time.sleep(1)
        del array
        time.sleep(1)
    array = np.ones((5000, 10000), dtype=np.float32)
    time.sleep(1)
    del array


if __name__ == '__main__':
    array_handler()
```

Package organisation:
```bash
|--- python_memory_profiler
	|--- plottrace.py
    |--- profiler.py
    |--- tools.py
| examples
	|---numpy_arrays_profiling.py
	|---profiler_data
        |--- array_handler  # Folder where the output of the example code are stored
