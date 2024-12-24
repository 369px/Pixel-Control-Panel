import psutil
import time

def print_system_info():
    """Printing system info on terminal each 5 seconds (cpu and memory)."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 ** 2)  # Convert to MB
        memory_total = memory.total / (1024 ** 2)  # Convert to MB

        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Used: {memory_used:.2f} MB / {memory_total:.2f} MB")
        print("-" * 40)
        time.sleep(5)
