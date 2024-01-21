import pickle
from pathlib import Path

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


def _convert_unit(value, unit, initial_unit="B"):
    UNITS = ["B", "kB", "MB", "GB", "TB"]
    magnitude = UNITS.index(unit)
    initial_magnitude = UNITS.index(initial_unit)
    return value / 1024 ** (magnitude - initial_magnitude)


def __process_trace_data(data, unit):
    data = np.array(data)

    timestamps = data[:, 0]
    timestamps -= timestamps[0]

    values = data[:, 1]
    values = _convert_unit(values, unit)
    return timestamps, values


def plot_metric(measurements, pid, path, title, unit, monitor, function_name):
    relative_timestamps, measurement_values = __process_trace_data(measurements, unit)

    plt.figure(figsize=(15, 7))
    plt.plot(relative_timestamps, measurement_values)

    plt.axhline(max(measurement_values), linestyle="dashdot", c="salmon")

    plt.grid()
    plt.xlabel("relative_time (s)")
    plt.ylabel(f"{monitor} ({unit})")

    max_lim = max(100, 1.05 * max(measurement_values))
    min_lim = -100
    plt.ylim(min_lim, max_lim)

    date = datetime.utcfromtimestamp(int(measurements[0][0])).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    plt.title(title + " - " + date)

    plt.savefig(path / f"memory_plot_{function_name}_{pid}_{monitor}.png", dpi=300)


def plot_trace(pid, path="data", title="", unit="MB", function_name=""):
    METRICS = ["data", "rss", "swap", "uss"]
    path = Path(path)
    for monitor in METRICS:
        filename = path / f"memory_profile_{pid}_{monitor}.dat"
        with open(filename, "rb") as current_file:
            read_measurements = pickle.load(current_file)
        plot_metric(read_measurements, pid, path, title, unit, monitor, function_name)
