import pickle
import sys
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def convert_unit(value, unit, initial_unit="B"):
    UNITS = ["B", "kB", "MB", "GB", "TB"]
    magnitude = UNITS.index(unit)
    initial_magnitude = UNITS.index(initial_unit)
    return value / 1024 ** (magnitude - initial_magnitude)

def __process_trace_data(data, unit):
    data = np.array(data)

    timestamps = data[:, 0]
    timestamps -= timestamps[0]

    values = data[:, 1]
    values = convert_unit(values, unit)
    return timestamps, values


def plot_trace(pid, path="./", title="", unit="MB"):
    QUANTITIES = ['data', 'rss', 'swap', 'uss']

    path = Path(path)

    for quantity in QUANTITIES:
        filename = path / f"memory_profile_{pid}_{quantity}.dat"
        with open(filename, "rb") as current_file:
            read_measurements = pickle.load(current_file)

        relative_timestamps, measurement_values = __process_trace_data(read_measurements, unit)

        fig = plt.figure(figsize=(15, 7))
        plt.plot(relative_timestamps, measurement_values)
        plt.grid()
        plt.xlabel("relative_time (s)")
        plt.ylabel(f"{quantity} ({unit})")
        max_lim = max(100, 1.03 * max(measurement_values))
        min_lim = -100
        plt.ylim(min_lim, max_lim)
        plt.title(title)
        plt.savefig(path / f"plot_{quantity}_memory_profile_{pid}.png", dpi=300)

if __name__ == "__main__":
    arguments = sys.argv
    pid = int(arguments[1])

    # TODO: use argparse
    path = arguments[2] if len(arguments) > 2 else "./"
    title = arguments[3] if len(arguments) > 3 else ""

    plot_trace(pid, path, title, unit = "MB")
