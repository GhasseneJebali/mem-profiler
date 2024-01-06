import psutil
import sys
import pickle
import time
from collections import defaultdict

if not (psutil.LINUX or psutil.MACOS or psutil.WINDOWS):
    sys.exit("platform not supported")

def profile_memory(pid: int, max_timer=0):
    process = psutil.Process(pid)
    measurements = defaultdict(list)

    frequency = 0.1
    QUANTITIES = ['data', 'rss', 'swap', 'uss']
    if max_timer:
        max_timer /= frequency
    step = 0
    print(f"Profiling memory usage of precess {pid}...")
    while step <= max_timer:
        try:
            mem_usage = process.memory_full_info()
            for quantity in QUANTITIES:
                measurements[quantity].append((time.time(), getattr(mem_usage, quantity)))

            if max_timer:
                step += 1

            time.sleep(frequency)
        except KeyboardInterrupt:
            break
        except psutil.NoSuchProcess:
            print(f"Process {pid} no longer active. Saving profiling data")
            break

    # dump measurements to files
    for quantity in QUANTITIES:
        with open(f"memory_profile_{pid}_{quantity}.dat", "wb") as current_file:
            pickle.dump(measurements[quantity], current_file)

if __name__ == "__main__":
    arguments = sys.argv
    pid = int(arguments[1])
    max_timer = int(arguments[2]) if len(arguments) > 2 else 0

    profile_memory(pid, max_timer)
