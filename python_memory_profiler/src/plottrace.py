import pickle
from pathlib import Path, PosixPath

from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np


def _convert_unit(value: np.ndarray, unit: str, initial_unit: str = "B"):
    """
    Converts a numerical value between units.

    Args:
        value (np.ndarray): Numerical values to be converted. 
        unit (str): Target unit for the conversion. 
            Must be one of ["B", "kB", "MB", "GB", "TB"].
        initial_unit (str, optional): Initial unit of the values. 
            Defaults to "B". Must also be one of ["B", "kB", "MB", "GB", "TB"].

    Returns:
        np.ndarray: Value(s) converted to the target unit.

    Raises:
        ValueError: If `unit` or `initial_unit` is not in the allowed units.

    Example:
        >>> value = np.array([1000, 2000])
        >>> _convert_unit(value, "MB", initial_unit="kB")
        array([1.0, 2.0])
    """
    UNITS = ["B", "kB", "MB", "GB", "TB"]
    magnitude = UNITS.index(unit)
    initial_magnitude = UNITS.index(initial_unit)
    return value / 1000 ** (magnitude - initial_magnitude)


def __process_trace_data(data: list[tuple], unit: str):
    """
    Processes trace data by normalizing timestamps and converting value units.

    Args:
        data (list[tuple]): A list of tuples where each tuple contains:
            - A timestamp (float or int).
            - A value (float or int) corresponding to the timestamp.
        unit (str): The target unit for the value conversion. 
            Must be one of ["B", "kB", "MB", "GB", "TB"].

    Returns:
        tuple: A tuple containing:
            - np.ndarray: Normalized timestamps (timestamps - first timestamp).
            - np.ndarray: Converted values in the specified unit.

    Example:
        >>> data = [(0, 1024), (1, 2048), (2, 4096)]
        >>> __process_trace_data(data, "kB")
        (array([0, 1, 2]), array([1.0, 2.0, 4.0]))

    Notes:
        - The first timestamp is used as the reference point for normalization.
    """
    data = np.array(data)

    timestamps = data[:, 0]
    timestamps -= timestamps[0]

    values = data[:, 1]
    values = _convert_unit(values, unit)
    return timestamps, values


def plot_metric(measurements: list[tuple], pid: int, path: PosixPath, title: str, unit: str, monitor: str, function_name: str):
    """
    Plots a time-series metric and saves the plot as an image.

    Args:
        measurements (list[tuple]): A list of tuples where each tuple consists of:
            - A timestamp (float or int).
            - A measurement value (float or int) corresponding to the timestamp.
        pid (int): The process ID associated with the measurements.
        path (PosixPath): The directory path where the plot image will be saved.
        title (str): The title of the plot.
        unit (str): The unit of the measurement values (e.g., "kB", "MB").
        monitor (str): The name of the metric being plotted (e.g., "Memory", "CPU").
        function_name (str): The name of the function that generated the measurements.

    Returns:
        None

    Side Effects:
        - Creates and saves a plot image at the specified file path.
    """
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

    date = datetime.fromtimestamp(int(measurements[0][0]), timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    plt.title(title + " - " + date)

    plt.savefig(path / f"memory_plot_{function_name}_{pid}_{monitor}.png", dpi=300)


def plot_trace(pid, path: str = "data", title: str = "", unit: str = "MB", function_name: str = ""):
    """
    Generates and saves time-series plots for various memory-related metrics of a process.

    Args:
        pid (int): The process ID for which the memory metrics are plotted.
        path (str): Directory where the memory profile files are stored. Defaults to "data".
        title (str): The title of the plots. Defaults to an empty string.
        unit (str): The unit of measurement for the metrics (e.g., "MB", "kB"). Defaults to "MB".
        function_name (str): The name of the function generating the metrics. 
            Used in plot filenames. Defaults to an empty string.

    Returns:
        None

    Side Effects:
        - Reads memory profile files for the given process from the specified path.
        - Generates and saves time-series plots for each metric in the file.

    Details:
        - The function processes four memory metrics: "data", "rss", "swap", and "uss".
        - For each metric:
          1. Reads its corresponding `.dat` file containing measurement data as a pickled object.
          2. Calls `plot_metric` to process the data and generate a plot.
          3. Saves the plot in the specified directory, with a filename format:
             `memory_plot_<function_name>_<pid>_<monitor>.png`.
    """
    METRICS = ["data", "rss", "swap", "uss"]
    path = Path(path)
    for monitor in METRICS:
        filename = path / f"memory_profile_{pid}_{monitor}.dat"
        with open(filename, "rb") as current_file:
            read_measurements = pickle.load(current_file)
        plot_metric(read_measurements, pid, path, title, unit, monitor, function_name)
