import psutil
import sys
import os
import pickle
import time
import logging
from pathlib import Path
from collections import defaultdict
from threading import Thread

from .plottrace import plot_metric


DEFAULT_PARAMETERS = {
    "max_timer": 0,
    "path": "profiler_data",
    "frequency": 0.1,
}

METRICS = ["data", "rss", "swap", "uss"]


class Profiler:
    def __init__(self, pid: int, function_name: str):
        self.pid = pid
        self.function_name = function_name

        self.max_timer = DEFAULT_PARAMETERS["max_timer"]
        self.path = Path(os.getcwd()) / DEFAULT_PARAMETERS["path"] / str(self.function_name)

        self.frequency = DEFAULT_PARAMETERS["frequency"]

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start(self):
        daemon = Thread(target=self._run_mem_prof, daemon=True, name="Profile")
        daemon.start()

    def _run_mem_prof(self):
        process = psutil.Process(self.pid)
        self.measurements = defaultdict(list)

        if self.max_timer:
            self.max_timer /= self.frequency
        step = 0
        if self.logger is not None:
            self.logger.info(f"Profiling memory usage for function {self.function_name} (pid {self.pid})...")
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

    def save(self, monitor=None):
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
                self.path / f"memory_profile_{self.function_name}_{self.pid}_{metric}.dat", "wb"
            ) as current_file:
                pickle.dump(self.measurements[metric], current_file)

    def plot(self, monitor=None):
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
                function_name= self.function_name,
            )
