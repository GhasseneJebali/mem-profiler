import sys
import os
import pickle
import time
import logging
from pathlib import Path
from collections import defaultdict
from threading import Thread

import psutil

from .plottrace import plot_metric


DEFAULT_PARAMETERS = {
    "max_timer": 0,
    "path": "profiler_data",
    "frequency": 0.1,  # in seconds
}

METRICS = ["data", "rss", "swap", "uss"]


class Profiler:
    """
    A class for profiling and analyzing the memory usage of a process over time.

    Attributes:
        pid (int): Process ID to monitor.
        function_name (str): Name of the function being profiled.
        max_timer (float): Maximum time (in seconds) to profile the process. Loaded from default parameters.
        path (Path): Directory where profiling data and plots will be saved.
        frequency (float): Sampling frequency (in seconds) for memory measurements. Loaded from default parameters.
        measurements (defaultdict): Dictionary to store memory measurements for different metrics.
        logger (logging.Logger): Logger instance for reporting profiling events.

    Methods:
        start():
            Starts a daemon thread to profile memory usage.

        save(monitor: str | None = None):
            Saves profiling data for the specified metrics to disk.

        plot(monitor: str | None = None):
            Generates and saves time-series plots for the specified memory metrics.
    """

    def __init__(self, pid: int, function_name: str):
        """
        Initializes the profiler with the given process ID and function name.

        Args:
            pid (int): The process ID to monitor.
            function_name (str): The name of the function being profiled.
        """
        self.pid = pid
        self.function_name = function_name

        self.max_timer = DEFAULT_PARAMETERS["max_timer"]
        self.path = (
            Path(os.getcwd()) / DEFAULT_PARAMETERS["path"] / str(self.function_name)
        )

        self.frequency = DEFAULT_PARAMETERS["frequency"]

        self.measurements = None

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start(self):
        """
        Starts the profiling process in a daemon thread.

        Notes:
            The profiler monitors memory usage in the background and records data periodically.
        """
        daemon = Thread(target=self._run_mem_prof, daemon=True, name="Profile")
        daemon.start()

    def _run_mem_prof(self):
        """
        Monitors memory usage of the specified process and records measurements.

        Notes:
            - Profiling continues until the process ends or the maximum timer expires.
        """
        process = psutil.Process(self.pid)
        self.measurements = defaultdict(list)

        if self.max_timer:
            self.max_timer /= self.frequency
        step = 0
        if self.logger is not None:
            self.logger.info(
                f"Profiling memory usage for function {self.function_name} (pid {self.pid})..."
            )
        while step <= self.max_timer:
            try:
                mem_usage = process.memory_full_info()
                for metric in METRICS:
                    self.measurements[metric].append(
                        (time.time(), getattr(mem_usage, metric))
                    )

                if self.max_timer:
                    step += 1

                time.sleep(self.frequency)
            except KeyboardInterrupt:
                break
            except psutil.NoSuchProcess:
                if self.logger is not None:
                    self.logger.info(f"Process {self.pid} no longer active.")
                break

    def save(self, monitor: str | None = None):
        """
        Saves profiling data to disk.

        Args:
            monitor (str | None): Specific metrics to save. If None, saves all metrics ["data", "rss", "swap", "uss"].

        Notes:
            - Files are saved in the `path` directory.
            - Filenames follow the format: `memory_profile_<function_name>_<pid>_<metric>.dat`.
        """
        if self.logger is not None:
            self.logger.info(f"Saving profiling data in {self.path}")
        # dump measurements to files
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        if not monitor:
            monitor = METRICS

        if not isinstance(monitor, list):
            monitor = [monitor]

        for metric in monitor:
            with open(
                self.path
                / f"memory_profile_{self.function_name}_{self.pid}_{metric}.dat",
                "wb",
            ) as current_file:
                pickle.dump(self.measurements[metric], current_file)

    def plot(self, monitor: str | None = None):
        """
        Generates and saves memory usage plots for the specified metrics.

        Args:
            monitor (str | None): Specific metrics to plot. If None, plots all metrics.

        Notes:
            - Plots are saved in the `path` directory.
            - Filenames follow the format: `memory_plot_<function_name>_<pid>_<metric>.png`.
        """
        if not monitor:
            monitor = METRICS

        if not isinstance(monitor, list):
            monitor = [monitor]

        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        for metric in monitor:
            title = f"Memory usage for {self.function_name} (pid {self.pid})"
            plot_metric(
                self.measurements[metric],
                pid=self.pid,
                path=self.path,
                title=title,
                unit="MB",
                monitor=metric,
                function_name=self.function_name,
            )
