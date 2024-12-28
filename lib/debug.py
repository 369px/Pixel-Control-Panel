import psutil
import os
import time

def print_system_info(page):
    """Print the app's CPU and memory usage on the terminal every 5 seconds."""
    # Ottieni il processo corrente
    current_process = psutil.Process(os.getpid())

    while True:
        # Utilizzo CPU e memoria del processo corrente
        cpu_usage = current_process.cpu_percent(interval=1)  # Percentuale CPU
        memory_info = current_process.memory_info()
        memory_used = memory_info.rss / (1024 ** 2)  # Memoria usata (RSS) in MB

        print(f"App Debug Info (Page: {page})")
        print(f"CPU Usage: {cpu_usage:.2f}%")
        print(f"Memory Used: {memory_used:.2f} MB")
        print("-" * 40)
        time.sleep(1)
