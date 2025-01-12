# Python Memory Profiler

Python Memory Profiler is a Python package designed for efficient and customizable memory usage monitoring of Python programs. It allows developers to track memory metrics such as data, RSS (Resident Set Size), swap usage, and USS (Unique Set Size) for specific functions in their applications.

## Features

- **Lightweight Memory Profiling**: Monitors memory metrics for specific functions.
- **Configurable Settings**: Adjustable sampling frequency and profiling duration.
- **Visualization**: Automatically generates plots of memory usage trends.
- **Data Persistence**: Saves memory metrics for further analysis.

## Installation

### From source
Clone the repository and install the dependencies:

```bash
$ git clone https://github.com/GhasseneJebali/python-memory-profiler.git
$ cd python-memory-profiler
$ pip install -e . -r requirements.txt
```

## Usage

### Decorator-Based Profiling

You can use the `@profile_memory_decorator` to profile memory usage for specific functions.

```python
from memory_profiler.decorators import memory_profiler_decorator

@memory_profiler_decorator
def my_function():
    # Your code here
    pass

if __name__ == "__main__":
    my_function()
```

This will:
- Monitor the memory usage of `my_function`.
- Save the memory metrics in the `data` folder.
- Generate a memory usage plot.

### Custom Profiling with `Profiler` Class

For more control, you can directly use the `Profiler` class:

```python
import os

from memory_profiler.src.profiler import Profiler


if __name__ == "__main__":
    
    pid = os.getpid()

    profiler = Profiler(pid, "my_function")
    profiler.start()

    # Your code here

    # If monitor is not specified, all metrics will be logged
    # Logged metrics are data, rss, uss and swap 
    profiler.save(monitor=None)
    profiler.plot(monitor=None)
```

### Configuration

You can adjust default profiling parameters such as sampling frequency and output path by modifying the `src/configs/config.yaml` configuration file:

```yaml
max_timer: 0  # Maximum time (in seconds) to profile the process
path: profiler_data  # Directory where profiling data and plots will be saved
frequency: 0.1   # Sampling frequency (in seconds)

metrics: ["data", "rss", "swap", "uss"]
```

For more information, check `Profiler` class documentation.

## Output

The profiling results are saved as `.dat` files in the specified output directory and as `.png` plots showing memory usage trends over time.

### Example Plot

![Memory Usage Example](examples/profiler_data/array_handler/memory_plot_array_handler_450155_data.png)

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Developed by [Ghassene Jebali](https://github.com/GhasseneJebali).
