import os
import time
import pickle
from memory_profiler.src.profiler import Profiler
from memory_profiler.src.plottrace import plot_metric


def test_profiler_initialization():
    """Test that the Profiler initializes correctly."""
    pid = os.getpid()
    function_name = "test_function"
    profiler = Profiler(pid, function_name)

    assert profiler.pid == pid, "Profiler PID should match the current process ID."
    assert profiler.function_name == function_name, "Profiler function name should match the input."
    assert profiler.max_timer is not None, "Profiler should initialize max_timer."
    assert profiler.frequency > 0, "Profiler frequency should be greater than 0."
    assert profiler.measurements is None, "Measurements should initially be None."


def test_profiler_save(tmp_path):
    """Test saving profiling data to the filesystem."""
    pid = os.getpid()
    function_name = "test_function"
    profiler = Profiler(pid, function_name)
    profiler.path = tmp_path
    profiler.measurements = {"data": [(time.time(), 100), (time.time(), 200)]}

    profiler.save("data")

    # Check that the file was created
    expected_file = tmp_path / f"memory_profile_{function_name}_{pid}_data.dat"
    assert expected_file.exists(), "Expected profiling data file to be created."

    # Verify file content
    with open(expected_file, "rb") as file:
        saved_data = pickle.load(file)
    assert saved_data == profiler.measurements["data"], "Saved data should match the profiler measurements."


def test_profiler_run_mem_prof():
    """Test the Profiler's memory profiling logic."""
    pid = os.getpid()
    function_name = "test_function"
    profiler = Profiler(pid, function_name)

    # Run memory profiling for a short time
    profiler.max_timer = 0.1  # Adjust timer for quick test
    profiler.frequency = 0.05
    profiler._run_mem_prof()

    # Ensure measurements were recorded
    assert profiler.measurements, "Measurements should not be empty after profiling."
    for metric, data in profiler.measurements.items():
        assert len(data) > 0, f"Measurements for {metric} should contain data."


def test_plot_metric(tmp_path):
    """Test the plot_metric function."""
    measurements = [(1.0, 100), (2.0, 150), (3.0, 200)]
    pid = os.getpid()
    title = "Test Metric Plot"
    unit = "MB"
    monitor = "rss"
    function_name = "test_function"

    # Call the function
    plot_metric(measurements, pid, tmp_path, title, unit, monitor, function_name)

    # Check that the plot file was created
    expected_file = tmp_path / f"memory_plot_{function_name}_{pid}_{monitor}.png"
    assert expected_file.exists(), "Expected plot file to be created."
